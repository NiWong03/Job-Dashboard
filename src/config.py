# config.py
import os
from dotenv import load_dotenv
load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")     
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Replace with the password you set for jobuser
DB_HOST = os.getenv("DB_HOST", "localhost")         # Usually localhost for local development            # Default PostgreSQL port
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")



# Construct the database URL
# DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL = "postgresql://jobsdb_woqz_user:lIFp4VmsFEDdf5hEOoVVqVa5WupoGVSV@dpg-d1vvcgfdiees73c2t5m0-a.oregon-postgres.render.com/jobsdb_woqz"