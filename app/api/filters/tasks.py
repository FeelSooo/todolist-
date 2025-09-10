from pydantic import BaseModel, ConfigDict, Field

class GetTasksFilter(BaseModel):
    done: bool | None = None # поиск сделано\не сделано
    q: str | None = None # поиск по подстроке
