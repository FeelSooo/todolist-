from dataclasses import dataclass
from typing import ClassVar

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db import get_session
from app.utils import get_repository
from app.repositories.tasks import TasksRepository
from app.schemas import GetTasksFilter


@dataclass
class TasksService:
    session: AsyncSession = Depends(get_session)
    tasks_repository: ClassVar[TasksRepository] = get_repository(TasksRepository)

    async def get_tasks(
        self,
        filters: GetTasksFilter,
    ):
        tasks = await self.tasks_repository.get_tasks(
            filters=filters,
        )
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": ["Tasks not found"]},
            )
        return tasks
