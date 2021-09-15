from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.dependencies.config import SETTINGS, AppEnv

if SETTINGS.app_env == AppEnv.test:
    connect_args = {'check_same_thread': False}
    engine = create_engine(SETTINGS.test_db_uri, connect_args=connect_args)
else:
    engine = create_engine(SETTINGS.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
