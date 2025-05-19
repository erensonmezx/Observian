# app/services/log_pruner.py
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import LogEvent

def prune_old_logs(days: int = 7):
    db: Session = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        deleted = db.query(LogEvent).filter(LogEvent.timestamp < cutoff).delete()
        db.commit()
        logging.info(f"✅ Pruned {deleted} log entries older than {days} days.")
    except Exception as e:
        logging.error(f"❌ Error during log pruning: {e}")
        db.rollback()
    finally:
        db.close()