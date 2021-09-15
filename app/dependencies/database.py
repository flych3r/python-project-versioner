from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.dependencies.config import SETTINGS, AppEnv

connect_args = {}
database_url = SETTINGS.database_url

if SETTINGS.app_env == AppEnv.test:
    connect_args = {'check_same_thread': False}
else:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

engine = create_engine(database_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
