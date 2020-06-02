from typing import Iterator

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas, slack
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Depends(get_db)


@app.get("/")
async def home() -> str:
    return "Hia!"


@app.get("/_slack")
async def slack_test(db: Session = db_dependency) -> int:
    report = db.query(models.Report).first()
    slack.notify(report)
    return 200


@app.post("/report", response_model=schemas.Report)
def report_view(report: schemas.Report, db: Session = db_dependency) -> models.Report:
    existing = (
        db.query(models.Report)
        .filter(
            models.Report.json_input == report.json_input,
            models.Report.python_output == report.python_output,
        )
        .first()
    )
    if existing:
        return existing

    db_report = models.Report(
        json_input=report.json_input, python_output=report.python_output
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    try:
        slack.notify(report)
    except Exception:
        pass

    return db_report
