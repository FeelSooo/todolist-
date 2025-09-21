from typing import Sequence


from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.models.task import Task
from app.api.filters.tasks import GetTasksFilter
from sqlalchemy import select


class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, filters: GetTasksFilter) -> Sequence[Task]:
        query = select(Task)
        if filters.done is not None:
            query = query.where(Task.done == filters.done)
        if filters.q:
            query = query.where(Task.title_ci.contains(filters.q.lower()))

        rows = await self.session.execute(query.order_by(Task.id.asc()))
        return rows.scalars().all()


    async def get_task_by_id(self, task_id: int) -> Task|None:
        res = await self.session.execute(select(Task).where(Task.id == task_id))
        return res.scalar_one_or_none()


    async def add(self, task:Task) -> None:
        self.session.add(task)

    
    