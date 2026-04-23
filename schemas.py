from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


# Scheams for the validation of the data sent to the api
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AllowedOrderBy(str, Enum):
    created_at = "created_at"
    due_date = "due_date"
    priority = "priority"
    updated_at = "updated_at"


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

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


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

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TodoUpdate(BaseModel):
    task: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority | None = None


class ResponseMessage(BaseModel):
    message: str


class Status(str, Enum):
    pending = "Pending"
    done = "Done"
