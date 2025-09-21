from pydantic import BaseModel


class GetTasksFilter(BaseModel):
    done: bool | None = None
    q: str | None = None
    