from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # for work with orm-objects
    id: int
    title: str
    done: bool
    created_at: datetime
    updated_at: datetime


class TaskEnvelope(BaseModel):
    result: TaskResponse


class TasksEnvelope(BaseModel):
    result: list[TaskResponse]
