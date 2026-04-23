
test_task_success = {
    "task": "Test task",
    "description": "Test description",
    "due_date": "2026-09-08T12:00:00",
    "priority": "medium"
}


def test_create_task_success(client):
    response = client.post("/todos", json=test_task_success)
    assert response.status_code == 200
    assert response.json()["task"] == test_task_success["task"]


def test_create_task_duplicate(client):
    client.post("/todos", json=test_task_success)
    response = client.post("/todos", json=test_task_success)
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


def test_soft_delete(client):
    # Create a task to delete
    response = client.post("/todos", json=test_task_success)
    task_id = response.json()["id"]
    # Soft delete the task
    response = client.delete(f"/todos/{task_id}/soft")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Task soft deleted: {test_task_success['task']}"


def test_update_task(client):
    # Create a task to update
    response = client.post("/todos", json=test_task_success)
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
