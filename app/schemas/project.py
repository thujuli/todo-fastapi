from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(min_length=4)
    description: str | None = Field(default=None, min_length=10)


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    user_id: int
