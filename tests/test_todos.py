import pytest


@pytest.fixture
def sample_task():
    return {
        "task": "Test task",
        "description": "Test description",
        "due_date": "2026-09-08T12:00:00",
        "priority": "medium"
    }


def test_create_task_success(client, sample_task):
    response = client.post("/todos", json=sample_task)
    assert response.status_code == 200
    assert response.json()["task"] == sample_task["task"]


def test_create_task_duplicate(client, sample_task):
    client.post("/todos", json=sample_task)
    response = client.post("/todos", json=sample_task)
    assert response.status_code == 409
    assert response.json()["message"] == "Task already exists"


def test_create_task_empty(client):
    response = client.post("/todos", json={"task": "  "})
    assert response.status_code == 400
    assert response.json()["message"] == "Task cannot be empty"


def test_get_task_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Task not found"


def test_soft_delete(client, sample_task):
    # Create a task to delete
    response = client.post("/todos", json=sample_task)
    task_id = response.json()["id"]
    # Soft delete the task
    response = client.delete(f"/todos/{task_id}/soft")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task soft deleted: {sample_task['task']}"


def test_update_task(client, sample_task):
    # Create a task to update
    response = client.post("/todos", json=sample_task)
    task_id = response.json()["id"]
    # Update the task
    updated_values = {
        "task": "Updated task",
        "description": "Updated description",
        "due_date": "2026-10-08T12:00:00",
        "priority": "high"
    }
    assert response.status_code == 200
    response = client.patch(f"/todos/{task_id}", json=updated_values)
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task updated: {updated_values['task']}"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_mark_done(client, sample_task):
    # Create a task to mark as done
    response = client.post("/todos", json=sample_task)
    task_id = response.json()["id"]
    assert response.status_code == 200
    response = client.put(f"/todos/{task_id}/done")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task marked as done: {sample_task['task']}"


def test_reopen_task(client, sample_task):
    # Create a task to reopen
    response = client.post("/todos", json=sample_task)
    task_id = response.json()["id"]
    assert response.status_code == 200
    response = client.put(f"/todos/{task_id}/reopen")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task reopened: {sample_task['task']}"


def test_hard_delete(client, sample_task):
    # Create a task to hard delete
    response = client.post("/todos", json=sample_task)
    task_id = response.json()["id"]
    assert response.status_code == 200
    response = client.delete(f"/todos/{task_id}")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task removed: {sample_task['task']}"
