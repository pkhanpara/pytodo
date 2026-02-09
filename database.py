from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.pool import StaticPool

# Patch create_engine to use StaticPool for in-memory SQLite to share connections
_original_create_engine = sqlalchemy.create_engine

def _patched_create_engine(*args, **kwargs):
    if "poolclass" not in kwargs:
        kwargs["poolclass"] = StaticPool
    return _original_create_engine(*args, **kwargs)

sqlalchemy.create_engine = _patched_create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Determine database path (sqlite file in project root)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "todo.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a DB session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
