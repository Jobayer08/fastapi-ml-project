import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Retry DB connection (important for Docker)
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ Database connected")
        break
    except Exception as e:
        print("⏳ Waiting for database...")
        time.sleep(3)
else:
    raise Exception("❌ Database connection failed")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()