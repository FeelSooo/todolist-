from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


SQL_ALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit = False)


def get_db():
    db: Session = session_local()
    try:
        yield db
    finally:
        db.close()