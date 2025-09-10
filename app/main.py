from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes.tasks import router as task_router
from app.db import async_engine
from app.models.task import Base


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # создание таблиц при старте (dev-режим; в prod лучше Alembic)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


# общий стейт
# app.state.tasks = {}
# app.state.id_seq = count()


# включаю эндпоинты
app.include_router(task_router)
