from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import sessionmaker, Session


SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
# engine = create_engine(
#     SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
#
#
# def get_db():
#     db: Session = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async_engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get session."""
    async with (
        async_engine.begin() as connection,
        async_session(bind=connection) as session,
    ):
        yield session
