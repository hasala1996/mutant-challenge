""" Dependencies file for database
"""

from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --- SQL ---
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""
Base class for all models in the database.
"""


def get_db():
    """
    Method for db instance
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
