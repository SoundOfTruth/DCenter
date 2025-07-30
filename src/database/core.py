from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings


engine = create_engine(settings.DATABASE_URL)
session_factory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
