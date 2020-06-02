from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return "Hia!"


@app.post("/report", response_model=schemas.Report)
def report_view(report: schemas.Report, db: Session = Depends(get_db)):
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

    return db_report
