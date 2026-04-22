from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoItem(BaseModel):
    task: str
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority | None = None


class TodoResponse(BaseModel):
    id: int
    task: str
    status: str
    due_date: datetime | None = None
    priority: Priority | None = None
    is_deleted: bool

    class Config:
        from_attributes = True
        populated_by_name = True


class TodoDetail(BaseModel):
    id: int
    task: str
    status: str
    created_at: datetime
    updated_at: datetime | None
    is_deleted: bool
    description: str | None
    due_date: datetime | None
    priority: Priority | None = None

    class Config:
        from_attributes = True


class TodoUpdate(BaseModel):
    task: str | None = None
    status: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority | None = None
