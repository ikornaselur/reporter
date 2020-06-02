from sqlalchemy import Column, DateTime, Integer, String, func

from .db import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, server_default=func.now())

    json_input = Column(String)
    python_output = Column(String)
