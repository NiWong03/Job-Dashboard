from sqlalchemy import Column, Integer, String, Date, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id           = Column(Integer, primary_key=True)
    source       = Column(String, nullable=True)
    title        = Column(String, nullable=False)
    company      = Column(String, nullable=False)
    location     = Column(String)
    date_posted  = Column(Date)
    date_scraped = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    url          = Column(String, unique=True)