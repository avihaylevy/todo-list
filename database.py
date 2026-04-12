from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

# Loading variables from .env
load_dotenv()


# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create connection engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for models
class Base(DeclarativeBase):
    pass


# Dependency, opans and closes DB requests per session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
