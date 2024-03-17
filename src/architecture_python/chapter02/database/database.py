from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.architecture_python.chapter02.database.orm import metadata, start_mappers

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL or "sqlite:///:memory:", connect_args={"check_same_thread": False})
metadata.create_all(engine)

start_mappers()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
