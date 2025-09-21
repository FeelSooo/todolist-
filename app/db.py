from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import sessionmaker, Session


SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

async_engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo = False
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """get session"""
    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()