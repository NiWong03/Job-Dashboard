# test_db.py
from models import Base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Job
from db_init import engine



Session = sessionmaker(bind=engine)
session = Session()

# Get total count
total_jobs = session.query(Job).count()
print(f"Total jobs in database: {total_jobs}")

# Show first 10 jobs
jobs = session.query(Job).all()

for job in jobs[:10]:
    print(f"{job.title} @ {job.company} ({job.location}) - Posted: {job.date_posted} - URL: {job.url}")

session.close()