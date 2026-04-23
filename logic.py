from sqlalchemy.orm import Session
from models import Todo
from datetime import timedelta, datetime, timezone
from exceptions import TaskAlreadyExistsException, TaskCannotBeEmptyException, TaskNotFoundException
from schemas import Status
import logging


logger = logging.getLogger(__name__)


# Add task function to database
def add_task(db: Session, task: str, description: str | None = None, due_date: str | None = None, priority: str | None = None):
    task = task.strip()
    existing = db.query(Todo).filter(Todo.task == task).first()
    if existing:
        raise TaskAlreadyExistsException()
    new_task = Todo(task=task, status=Status.pending,
                    description=description, due_date=due_date, priority=priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info(f"Task added: {new_task.task}")
    return new_task


# View a task function from database, with oprional status filter and pagnation
def view_task(db: Session, status: str = None, after_id: int = 0, limit: int = 10, order_by: str = "created_at",
              priority: str = None, due_date: datetime | None = None, due_soon: bool = False, is_deleted: bool = False):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)
    if after_id:
        query = query.filter(Todo.id > after_id)
    if priority:
        query = query.filter(Todo.priority == priority)
    if due_date:
        query = query.filter(Todo.due_date <= due_date)
    if due_soon:
        query = query.filter(
            Todo.due_date >= datetime.now(timezone.utc),
            Todo.due_date <= datetime.now(timezone.utc) + timedelta(days=3))

    query = query.filter(Todo.is_deleted == False)
    return query.order_by(getattr(Todo, order_by)).limit(limit).all()


# view a task by id
def view_task_by_id(db: Session, task_id: int):
    return db.query(Todo).filter(Todo.id == task_id).first()


# Remove task function from db by id
def remove_task(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise TaskNotFoundException()
    db.delete(task)
    db.commit()
    logger.info(f"Task removed: {task.task}")
    return {"message": f"Task removed: {task.task}"}


# Mark as done function by id
def mark_done(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise TaskNotFoundException()
    task.status = Status.done
    db.commit()
    db.refresh(task)
    logger.info(f"Task marked as done: {task.task}")
    return {"message": f"Task marked as done: {task.task}"}


# Update a task by id, only fields that are sent will be updated
def update_task(db: Session, task_id: int, task: str | None = None, description: str | None = None,
                due_date: datetime | None = None, priority: str | None = None):
    existing_task = db.query(Todo).filter(Todo.id == task_id).first()
    if not existing_task:
        raise TaskNotFoundException()
    if task is not None and task.strip() == "":
        raise TaskCannotBeEmptyException()
    if task is not None:
        task = task.strip()
        duplicate = db.query(Todo).filter(
            Todo.task == task, Todo.id != task_id).first()
        if duplicate:
            raise TaskAlreadyExistsException()
        existing_task.task = task
    if description is not None:
        existing_task.description = description
    if due_date is not None:
        existing_task.due_date = due_date
    if priority is not None:
        existing_task.priority = priority
    db.commit()
    db.refresh(existing_task)
    logger.info(f"Task updated: {existing_task.task}")
    return {"message": f"Task updated: {existing_task.task}"}


# Soft delete a task, keeping it in the database but marking it as deleted
def soft_deleted(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise TaskNotFoundException()
    task.is_deleted = True
    db.commit()
    db.refresh(task)
    logger.info(f"Task soft deleted: {task.task}")
    return {"message": f"Task soft deleted: {task.task}"}


# Reopen a task changing its status back to pending
def reopen_task(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise TaskNotFoundException()
    task.status = Status.pending
    db.commit()
    db.refresh(task)
    logger.info(f"Task reopened: {task.task}")
    return {"message": f"Task reopened: {task.task}"}
