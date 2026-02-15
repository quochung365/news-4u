"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
from config.settings import settings
from models import Base


logger = logging.getLogger(__name__)

DATABASE_URL = settings.DATABASE_URL
logger.info(f"Using database: {DATABASE_URL}")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database (create tables if not exist).
    """
    Base.metadata.create_all(bind=engine)