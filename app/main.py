from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes.tasks import router as task_router
from app.db import async_engine
from app.models.task import Base


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # creating tables at the start (dev-mode, in the prod Alembic is better)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

# общий стейт
# app.state.tasks = {}
# app.state.id_seq = count()    


#включаю эндпоинты
app.include_router(task_router)