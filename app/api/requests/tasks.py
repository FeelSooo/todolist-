from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1)


class UpdateTaskRequest(BaseModel):
    done: bool | None = None
    title: str | None = Field(default=None, min_length=1)


class GetTasksFilter(BaseModel):
    done: bool | None = None
    q: str | None = None
