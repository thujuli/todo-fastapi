from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=4)
    description: str | None = Field(default=None, min_length=8)
    is_done: bool = Field(default=False)
    project_id: int


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
