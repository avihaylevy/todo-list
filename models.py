
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base
from schemas import Status, Priority


class Todo(Base):
    # Table name in db
    __tablename__ = "todos"

    # Unique id for each task
    id = Column(Integer, primary_key=True, index=True)

    # Task required and cannot cant be null
    task = Column(String, nullable=False)

    # Defualt task status is pending
    status = Column(String, default=Status.pending.value, index=True)

    # Setting the time the taske has being made
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Updated at the time the user updates it
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Checks if the task was deleted
    is_deleted = Column(Boolean, default=False, index=True)

    # optinal task description, can be null
    description = Column(String, nullable=True)

    # optional task due date, can be null
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)

    # optional task priority, default is 0
    priority = Column(String, default=Priority.low.value, index=True)
