# app/db/init_db.py

from app.models.models import Base
from app.db.database import engine

# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")