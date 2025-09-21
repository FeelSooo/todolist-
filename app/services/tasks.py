from dataclasses import dataclass
from typing import ClassVar

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.models.task import Task
from app.utils import get_repository
from app.repositories.tasks import TasksRepository
from app.api.filters.tasks import GetTasksFilter
from app.api.requests.tasks import TaskCreate, TaskUpdate
from app.api.responses.tasks import TaskResponse
from app.models.task import Task


@dataclass
class TasksService:
    session: AsyncSession = Depends(get_session)
    tasks_repository: ClassVar[TasksRepository] = get_repository(TasksRepository)

    async def get_tasks(
        self,
        filters: GetTasksFilter,
    ) -> list[TaskResponse]:
        tasks = await self.tasks_repository.get_tasks(filters=filters)
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": ["Tasks not found"]},
            )
        return [TaskResponse.model_validate(t) for t in tasks]

    async def get_task(
        self,
        task_id: int,
    ) -> TaskResponse:
        task = await self.tasks_repository.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found"
            )
        return TaskResponse.model_validate(task)

    async def patch_task(
        self,
        task_id: int,
        data: TaskUpdate,
    ) -> TaskResponse:
        task = await self.tasks_repository.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        updated_task = await self.tasks_repository.update(
            task_id=task_id,
            title=data.title,
            done=data.done,
        )

        return TaskResponse.model_validate(updated_task)

    async def create_tasks(
        self,
        req: TaskCreate,
    ) -> dict[str, Task]:
        task = await self.tasks_repository.create(
            title=req.title,
            title_ci=req.title.lower(),
        )

        return {"result": task}

    async def delete_task(self, task_id: int) -> None:
        async with self.session.begin():
            task = await self.tasks_repository.get_task_by_id(task_id)
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="not found"
                )
            await self.session.delete(task)
            try:
                await self.session.flush()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="невозможно удалить"
                )

    @classmethod
    def provider(cls, session: AsyncSession = Depends(get_session)):
        return cls(session=session)
