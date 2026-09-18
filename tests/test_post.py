import pytest


def test_create_task(client, task_payload):
    response = client.request("POST", "/tasks", json=task_payload)
    assert response.status_code == 201
    task = response.json()
    assert set(task) == {"id", "title", "completed"}
    assert isinstance(task["id"], int)
    assert task["title"] == task_payload["title"]
    assert task["completed"] is False
    saved = client.request("GET", f"/tasks/{task['id']}")
    assert saved.status_code == 200
    assert saved.json() == task


@pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": "   "}, {"title": 123}])
def test_reject_invalid_title(client, payload):
    response = client.request("POST", "/tasks", json=payload)
    assert response.status_code == 400
    assert response.json() == {"error": "Title must be a non-empty string"}
    assert client.request("GET", "/tasks").json() == []


def test_reject_invalid_completed_type(client):
    response = client.request("POST", "/tasks", json={"title": "Task", "completed": "yes"})
    assert response.status_code == 400
    assert response.json() == {"error": "Completed must be a boolean"}


def test_reject_malformed_json(client):
    response = client.request("POST", "/tasks", data="{broken", headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid JSON"}


def test_reject_non_object_json(client):
    response = client.request("POST", "/tasks", json=["Task"])
    assert response.status_code == 400
    assert response.json() == {"error": "JSON must be an object"}


def test_reject_wrong_content_type(client):
    response = client.request("POST", "/tasks", data="title=Task")
    assert response.status_code == 415
    assert response.json() == {"error": "Use application/json"}
