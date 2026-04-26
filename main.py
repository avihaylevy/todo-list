from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import AllowedOrderBy, ResponseMessage, TodoDetail, TodoItem, TodoResponse, TodoUpdate, Status, Priority
import logic
from exceptions import TaskAlreadyExistsException, TaskCannotBeEmptyException, TaskNotFoundException

# Create tables in database automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=[
    {"name": "Read"},
    {"name": "Create"},
    {"name": "Update"},
    {"name": "Delete"},
])


# Return a custom error message for Task not found
@app.exception_handler(TaskNotFoundException)
async def task_not_found_exception(request, exc):
    return JSONResponse(status_code=404, content={"message": "Task not found"})


# Return a custom error message for Task cannot be empty
@app.exception_handler(TaskCannotBeEmptyException)
async def task_cannot_be_empty_exception(request, exc):
    return JSONResponse(status_code=400, content={"message": "Task cannot be empty"})


# Return a custom error message for Task already exists
@app.exception_handler(TaskAlreadyExistsException)
async def task_already_exists_exception(request, exc):
    return JSONResponse(status_code=409, content={"message": "Task already exists"})


# Serve the html ui
@app.get("/", response_class=HTMLResponse, tags=["Read"])
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to query the database to check if its connected
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB down: {e}")


# When a get request is sent to /todos, return all tasks, with optional status fillter and pagnation
@app.get("/todos", response_model=list[TodoResponse], response_model_exclude_none=False, tags=["Read"])
def get_tasks(
        status: Status | None = None,
        after_id: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        order_by: AllowedOrderBy = AllowedOrderBy.created_at,
        priority: Priority | None = None,
        due_date: datetime | None = None,
        due_soon: bool = False):

    return logic.view_task(
        db,
        status=status,
        after_id=after_id,
        limit=limit,
        order_by=order_by,
        priority=priority,
        due_date=due_date,
        due_soon=due_soon)


# When a get request is sent to /todos/(task_id), return that task
@app.get("/todos/{task_id}", response_model=TodoDetail, tags=["Read"])
def get_task_by_id(
        task_id: int,
        db: Session = Depends(get_db)):
    task = logic.view_task_by_id(db, task_id=task_id)
    if not task:
        # 404 = Not fount if task with that id does not exist
        raise TaskNotFoundException()
    return task


# When a post request is sent to /tasks, create a task
@app.post("/todos", tags=["Create"], response_model=TodoResponse)
def create_task(
        item: TodoItem,
        db: Session = Depends(get_db)):
    # 400 = Bad request if task empty
    if not item.task or item.task.strip() == "":
        raise TaskCannotBeEmptyException()
    result = logic.add_task(
        db,
        item.task,
        item.description,
        item.due_date,
        item.priority)
    return result


# When a delete request is sent to /todos/(task_id)/soft. mark it as deleted without removing it from the database
@app.delete("/todos/{task_id}/soft", tags=["Delete"], response_model=ResponseMessage)
def soft_delete(
        task_id: int,
        db: Session = Depends(get_db)):
    result = logic.soft_deleted(db, task_id)
    return result


# When a delete request is sent with a task number, remove that task
@app.delete("/todos/{task_id}", tags=["Delete"], response_model=ResponseMessage)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db)):
    result = logic.remove_task(db, task_id)
    return result


# when a patch request is sent, uptdate that task with the new data, only fields that are sent will be updated, the rest will be  left unchanged
@app.patch("/todos/{task_id}", tags=["Update"], response_model=ResponseMessage)
def update_task(task_id: int, item: TodoUpdate, db: Session = Depends(get_db)):
    result = logic.update_task(
        db,
        task_id=task_id,
        task=item.task,
        description=item.description,
        due_date=item.due_date,
        priority=item.priority)
    return result


# When a PUT request is sent to /tasks/(task index)/done, mark that task as done
@app.put("/todos/{task_id}/done", tags=["Update"], response_model=ResponseMessage)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.mark_done(db, task_id)
    return result


# When a PUT request is sent to /tasks/(task index)/reopen, mark that task as pending if it was marked as done
@app.put("/todos/{task_id}/reopen", tags=["Update"], response_model=ResponseMessage)
def reopen_task(task_id: int, db: Session = Depends(get_db)):
    result = logic.reopen_task(db, task_id)
    return result
