# app/maintenance/prune_old_logs.py

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import LogEvent
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def prune_logs(days: int = 7):
    cutoff = datetime.utcnow() - timedelta(days=days)
    db = SessionLocal()
    try:
        deleted = db.query(LogEvent).filter(LogEvent.timestamp < cutoff).delete()
        db.commit()
        print(f"[PRUNE] Deleted {deleted} old log entries (older than {days} days).")
    finally:
        db.close()

if __name__ == "__main__":
    prune_logs()