# test_connection.py
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:observian@localhost:5432/observian")

try:
    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL!")
except Exception as e:
        print("❌ Failed:", e)