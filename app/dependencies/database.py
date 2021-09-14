from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.dependencies.config import SETTINGS, AppEnv

if SETTINGS.app_env == AppEnv.test:
    engine = create_engine(SETTINGS.test_db_uri)
else:
    engine = create_engine(SETTINGS.db_uri)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
