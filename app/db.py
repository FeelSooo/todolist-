from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)


SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

async_engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, echo = False
)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """get session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()