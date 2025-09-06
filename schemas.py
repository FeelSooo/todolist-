from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(...,min_length=1)


class TaskPatch(BaseModel):
    done: bool | None = None
    # todo
    # sdelat' dlya samoi taski toje izmenenya :)
    # new_title: str | None


class GetTasksFilter(BaseModel):
    done: bool | None = None # поиск сделано\не сделано
    q: str | None = None # поиск по подстроке