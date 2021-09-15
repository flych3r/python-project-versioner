from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.dependencies.config import SETTINGS, AppEnv

if SETTINGS.app_env == AppEnv.test:
    connect_args = {'check_same_thread': False}
    db_url = SETTINGS.test_db_uri
else:
    db_url = SETTINGS.database_url.replace('postgres://', 'postgresql://')
    connect_args = {}
engine = create_engine(db_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
