from sqlalchemy.orm import Session
from models import Todo


# Add task function to database
def add_task(db: Session, task: str):
    new_task = Todo(task=task, status="pending")
    existing = db.query(Todo).filter(Todo.task == task).first()
    if existing:
        return {"error": "Task already exists"}
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# View a task function from database, with oprional status filter and pagnation
def view_task(db: Session, status: str = None, skip: int = 0, limit: int = 10):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)

    return query.offset(skip).limit(limit).all()


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
