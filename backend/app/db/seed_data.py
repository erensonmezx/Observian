# app/db/seed_data.py

from sqlalchemy.orm import Session
from app.models.models import Service, LogEvent
from app.db.database import SessionLocal
from datetime import datetime, timedelta, timezone
import random

def seed_services(db:Session):
    if db.query(Service).count() > 0:
        print("✅ Services already exist. Skipping seeding.")
        return
    services = [
        Service(name='auth-services', team_owner='Identity Team'),
        Service(name='checkout-service', team_owner='Payments Team'),
        Service(name="inventory-service", team_owner="Ops Team")
    ]
    db.add_all(services)
    db.commit()
    
    
def seed_log_events(db:Session):

    services = db.query(Service).all()
    now = datetime.now(timezone.utc)

    for service in services:
        for i in range(10):
            log = LogEvent(
                service_id= service.id,
                timestamp= now - timedelta(minutes=i*5),
                status_code= random.choice([200, 500, 502, 403]),
                latency_ms= random.uniform(50.0, 300.0)
            )
            db.add(log)
    db.commit()
    
    
def main():
    db= SessionLocal()
    try:
        seed_services(db)
        seed_log_events(db)
        print("Test data seeded.")
    finally:
        db.close()
        
if __name__ == '__main__':
    main()
    