from typing import Sequence


from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.models.task import Task
from app.api.filters.tasks import GetTasksFilter
from sqlalchemy import select, insert, Result, update


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

    async def get_task_by_id(
        self,
        task_id: int,
    ) -> Task | None:
        res = await self.session.execute(
            select(
                Task,
            ).where(
                Task.id == task_id,
            ),
        )
        return res.scalar_one_or_none()

    async def add(
        self,
        task: Task,
    ) -> None:
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)

    async def create(
        self,
        title: str,
        title_ci: str,
    ) -> Task:
        query = (
            insert(
                Task,
            )
            .values(
                title=title,
                title_ci=title_ci,
            )
            .returning(
                Task,
            )
        )
        result: Result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(
        self,
        task_id: int,
        title: str,
        done: bool,
    ) -> Task:
        query = (
            update(
                Task,
            )
            .where(
                Task.id == task_id,
            )
            .returning(
                Task,
            )
        )
        if title:
            query = query.values(title=title)
        if done:
            query = query.values(done=True)

        result: Result = await self.session.execute(query)
        return result.scalar_one_or_none()
