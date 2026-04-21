
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class Todo(Base):
    # Table name in db
    __tablename__ = "todos"

    # Unique id for each task
    id = Column(Integer, primary_key=True, index=True)

    # Task required and cannot cant be null
    task = Column(String, nullable=False)

    # Defualt task status is pending
    status = Column(String, default="pending")

    # Setting the time the taske has being made
    created_at = Column(DateTime, server_default=func.now())

    # Updated at the time the user updates it
    updated_at = Column(DateTime, onupdate=func.now())

    # Checks if the task was deleted
    is_deleted = Column(Boolean, default=False)
