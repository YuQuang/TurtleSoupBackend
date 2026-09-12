from uuid import UUID
from pydantic import BaseModel, Field


class CreateStoryDTO(BaseModel):
    title: str = Field(min_length=1)
    mystery: str = Field(min_length=1)
    solution: str = Field(min_length=1)
    hint: str = Field(min_length=1)
    is_published: bool = Field(default=False)


class UpdateStoryDTO(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    mystery: str = Field(min_length=1)
    solution: str = Field(min_length=1)
    hint: str = Field(min_length=1)
    is_published: bool = Field(default=False)