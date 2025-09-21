from pydantic import BaseModel, Field, model_validator


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    done: bool | None = None
    title: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.title is None and self.done is None:
            raise ValueError("Хотя бы одно поле должно быть заполнено")
        return self



class GetTasksFilter(BaseModel):
    done: bool | None = None
    q: str | None = None
