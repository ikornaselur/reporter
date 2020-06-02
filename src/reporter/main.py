import os
from typing import Iterator

import sentry_sdk
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas, slack
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

if sentry_dsn := os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(sentry_dsn)


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


@app.post("/pytyper", response_model=schemas.Report)
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
        slack.notify(db_report)
    except Exception:
        sentry_sdk.capture_exception()

    return db_report
