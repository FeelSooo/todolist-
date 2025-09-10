from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db import get_session
from app.models.task import Task
from app.schemas import GetTasksFilter
from sqlalchemy import select


class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(
        self,
        filters: GetTasksFilter,
    ):
        query = select(Task)
        if filters.done is not None:
            query = query.where(Task.done == filters.done)
        if filters.q:
            query = query.where(Task.title_ci.contains(filters.q.lower()))

        rows = await self.session.execute(query.order_by(Task.id.asc()))
        return rows.scalars().all()
