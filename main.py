from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import TodoItem
import logic

# Create tables in database automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Serve the html ui
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


# When a get request is sent to /todos, return all tasks, with optional status fillter and pagnation
@app.get("/todos")
def get_tasks(status: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return logic.view_task(db, status=status, skip=skip, limit=limit)


# When a get request is sent to /todos/(task_id), return that task
@app.get("/todos/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = logic.view_task_by_id(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# When a post request is sent to /tasks, create a task
@app.post("/todos")
def create_task(item: TodoItem, db: Session = Depends(get_db)):
    # 400 = Bad request if task empty
    if not item.task or item.task.strip() == "":
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    result = logic.add_task(db, item.task)
    # 409 = If the task already exists throw a conflict error
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    return result


# When a delete request is sent with a task number, remove that task
@app.delete("/todos/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.remove_task(db, task_id)
    if "error" in result:
        # Not found
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# When a PUT request is sent to /tasks/(task index)/done, mark that task as done
@app.put("/todos/{task_id}/done")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.mark_done(db, task_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
