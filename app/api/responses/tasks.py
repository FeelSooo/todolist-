from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # чтобы начать работать с ORM-объектами
    id: int
    title: str
    done: bool
    created_at: datetime
    updated_at: datetime


class TasksRequest(BaseModel):
    result: list[TaskResponse]
