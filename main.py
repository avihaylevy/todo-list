from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import TodoDetail, TodoItem, TodoResponse, TodoUpdate
import logic

# Create tables in database automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=[
    {"name": "Read"},
    {"name": "Create"},
    {"name": "Update"},
    {"name": "Delete"},
])


# Serve the html ui
@app.get("/", response_class=HTMLResponse, tags=["Read"])
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


# When a get request is sent to /todos, return all tasks, with optional status fillter and pagnation
@app.get("/todos", response_model=list[TodoResponse], response_model_exclude_none=False, tags=["Read"])
def get_tasks(status: str = None, after_id: int = 0, limit: int = 10, db: Session = Depends(get_db), order_by: str = "created_at", priority: str = None, due_date: datetime | None = None):
    return logic.view_task(db, status=status, after_id=after_id, limit=limit, order_by=order_by, priority=priority, due_date=due_date)


# When a get request is sent to /todos/(task_id), return that task
@app.get("/todos/{task_id}", response_model=TodoDetail, tags=["Read"])
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = logic.view_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# When a post request is sent to /tasks, create a task
@app.post("/todos", tags=["Create"])
def create_task(item: TodoItem, db: Session = Depends(get_db)):
    # 400 = Bad request if task empty
    if not item.task or item.task.strip() == "":
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    result = logic.add_task(
        db, item.task, item.description, item.due_date, item.priority)
    # 409 = If the task already exists throw a conflict error
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    return result


# When a delete request is sent to /todos/(task_id)/soft. mark it as deleted without removing it from the database
@app.delete("/todos/{task_id}/soft", tags=["Delete"])
def soft_delete(task_id: int, db: Session = Depends(get_db)):
    result = logic.soft_deleted(db, task_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# When a delete request is sent with a task number, remove that task
@app.delete("/todos/{task_id}", tags=["Delete"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.remove_task(db, task_id)
    if "error" in result:
        # Not found
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# when a pathc request is sent, uptdate that task with the new data, only fields that are sent will be updated, the rest will be  left unchanged
@app.patch("/todos/{task_id}", tags=["Update"])
def update_task(task_id: int, item: TodoUpdate, db: Session = Depends(get_db)):
    result = logic.update_task(db, task_id=task_id, task=item.task,
                               description=item.description, due_date=item.due_date, priority=item.priority)
    if "error" in result:
        if result["error"] == "Task not found":
            raise HTTPException(status_code=404, detail=result["error"])
        elif result["error"] == "Task cannot be empty":
            raise HTTPException(status_code=400, detail=result["error"])
        elif result["error"] == "Task already exists":
            raise HTTPException(status_code=409, detail=result["error"])
    return result


# When a PUT request is sent to /tasks/(task index)/done, mark that task as done
@app.put("/todos/{task_id}/done", tags=["Update"])
def complete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.mark_done(db, task_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/todos/{task_id}/reopen", tags=["Update"])
def reopen_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.reopen_task(db, task_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
