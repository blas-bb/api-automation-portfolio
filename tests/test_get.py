def test_get_empty_task_list(client):
    response = client.request("GET", "/tasks")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == []


def test_get_created_task(client, created_task):
    response = client.request("GET", f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task
    assert isinstance(response.json()["id"], int)


def test_get_task_list(client, created_task):
    response = client.request("GET", "/tasks")
    assert response.status_code == 200
    assert response.json() == [created_task]


def test_get_missing_task(client):
    response = client.request("GET", "/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found"}


def test_get_invalid_id(client):
    response = client.request("GET", "/tasks/abc")
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid task ID"}
