from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CreateTaskRequest(BaseModel):
    title: str = Field(...,min_length=1)


class UpdateTaskRequest(BaseModel):
    done: bool | None = None
    title: str | None = Field(default=None, min_length=1)
    # todo
    # sdelat' dlya samoi taski toje izmenenya :)
    # new_title: str | None


class GetTasksFilter(BaseModel):
    done: bool | None = None # поиск сделано\не сделано
    q: str | None = None # поиск по подстроке

