from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Job
from config import DATABASE_URL
from datetime import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def upsert_job(data):
    session = Session()
    try:
        # Duplicate check
        existing = session.query(Job).filter_by(
            url=data["url"],
            date_posted=data["date_posted"]
        ).first()
        
        if not existing:
            job = Job(**data)
            session.add(job)
            session.commit()
            print(f"[+] Added: {data['title']} at {data['company']}")
        else:
            print(f"[=] Skipped: {data['title']} at {data['company']} (already exists)")
            
    except Exception as e:
        print(f"[!] Error inserting job: {data['title']} – {e}")
        session.rollback()
    finally:
        session.close()

def clear_jobs():
    session = Session()
    try:
        num_deleted = session.query(Job).delete()
        session.commit()
        print(f"Deleted {num_deleted} jobs from the database.")
    except Exception as e:
        print(f"Error deleting jobs: {e}")
        session.rollback()
    finally:
        session.close()

def drop_all_tables():
    Base.metadata.drop_all(engine)
    print("All tables dropped.")

if __name__ == "__main__":
    clear_jobs()
    drop_all_tables()