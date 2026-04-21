from pydantic import BaseModel
from datetime import datetime


class TodoItem(BaseModel):
    task: str


class TodoResponse(BaseModel):
    id: int
    task: str
    status: str
    is_deleted: bool

    class Config:
        from_attributes = True


class TodoDetail(BaseModel):
    id: int
    task: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True


class TodoUpdate(BaseModel):
    id: int
    task: str | None = None
    created_at: datetime
    updated_at: datetime
