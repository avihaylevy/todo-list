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


# When a get request is sent to /tasks, return all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return logic.view_task(db)


# When a post request is sent to /tasks, create a task
@app.post("/tasks")
def create_task(item: TodoItem, db: Session = Depends(get_db)):
    # 400 = Bad request if empty
    if not item.task or item.task.strip() == "":
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    return logic.add_task(db, item.task)


# When a delete request is sent with a task number, remove that task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.remove_task(db, task_id)
    if "error" in result:
        # Not found
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# When a PUT request is sent to /tasks/(task index)/done, mark that task as done
@app.put("/tasks/{task_id}/done")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.mark_done(db, task_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
