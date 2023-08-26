from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

DB_URL = (
    "postgresql://"
    + settings.db_username
    + ":"
    + settings.db_password
    + "@"
    + settings.db_host
    + ":"
    + settings.db_port
    + "/"
    + settings.db_name
)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
