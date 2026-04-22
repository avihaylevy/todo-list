from sqlalchemy.orm import Session
from models import Todo
from datetime import timedelta, datetime


# Add task function to database
def add_task(db: Session, task: str, description: str | None = None, due_date: str | None = None, priority: str | None = None):
    existing = db.query(Todo).filter(Todo.task == task).first()
    if existing:
        return {"error": "Task already exists"}
    new_task = Todo(task=task, status="pending",
                    description=description, due_date=due_date, priority=priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# View a task function from database, with oprional status filter and pagnation
def view_task(db: Session, status: str = None, after_id: int = 0, limit: int = 10, order_by: str = "created_at", priority: str = None, due_date: datetime | None = None, is_deleted: bool = False):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)
    if after_id:
        query = query.filter(Todo.id > after_id)
    if priority:
        query = query.filter(Todo.priority == priority)
    if due_date:
        query = query.filter(
            Todo.due_date >= datetime.now(),
            Todo.due_date <= datetime.now() + timedelta(days=3))
    query = query.filter(Todo.is_deleted == False)
    return query.order_by(getattr(Todo, order_by)).limit(limit).all()


# view a task by id
def view_task_by_id(db: Session, task_id: int):
    return db.query(Todo).filter(Todo.id == task_id).first()


# Remove task function from db by id
def remove_task(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    db.delete(task)
    db.commit()
    return {"message": f"Task removed: {task.task}"}


# Mark as done function by id
def mark_done(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.status = "Done"
    db.commit()
    db.refresh(task)
    return {"message": f"Task marked as done: {task.task}"}


def update_task(db: Session, task_id: int, task: str | None = None, description: str | None = None, due_date: datetime | None = None, priority: str | None = None):
    existing_task = db.query(Todo).filter(Todo.id == task_id).first()
    if not existing_task:
        return {"error": "Task not found"}
    if task is not None and task.strip() == "":
        return {"error": "Task cannot be empty"}
    if task is not None:
        duplicate = db.query(Todo).filter(
            Todo.task == task, Todo.id != task_id).first()
        if duplicate:
            return {"error": "Another task with the same name already exists"}
        existing_task.task = task
    if description is not None:
        existing_task.description = description
    if due_date is not None:
        existing_task.due_date = due_date
    if priority is not None:
        existing_task.priority = priority
    db.commit()
    db.refresh(existing_task)
    return {"message": f"Task updated: {existing_task.task}"}


# Soft delete a task, keeping it in the database but marking it as deleted
def soft_deleted(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.is_deleted = True
    db.commit()
    db.refresh(task)
    return {"message": f"Task soft deleted: {task.task}"}


# Reopen a task changing its status back to pending
def reopen_task(db: Session, task_id: int):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.status = "pending"
    db.commit()
    db.refresh(task)
    return {"message": f"Task reopened: {task.task}"}
