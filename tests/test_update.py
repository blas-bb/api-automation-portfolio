import pytest


def test_put_replaces_task(client, created_task):
    path = f"/tasks/{created_task['id']}"
    client.request("PATCH", path, json={"completed": True})
    response = client.request("PUT", path, json={"title": "Replaced task"})
    expected = {"id": created_task["id"], "title": "Replaced task", "completed": False}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.request("GET", path).json() == expected


def test_patch_preserves_other_fields(client, created_task):
    path = f"/tasks/{created_task['id']}"
    response = client.request("PATCH", path, json={"completed": True})
    expected = {**created_task, "completed": True}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.request("GET", path).json() == expected


@pytest.mark.parametrize("method", ["PUT", "PATCH"])
def test_update_missing_task(client, method):
    response = client.request(method, "/tasks/999", json={"title": "Missing"})
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found"}


@pytest.mark.parametrize("method", ["PUT", "PATCH"])
def test_update_invalid_title_keeps_original(client, created_task, method):
    path = f"/tasks/{created_task['id']}"
    response = client.request(method, path, json={"title": ""})
    assert response.status_code == 400
    assert response.json() == {"error": "Title must be a non-empty string"}
    assert client.request("GET", path).json() == created_task


def test_patch_rejects_unknown_field(client, created_task):
    response = client.request("PATCH", f"/tasks/{created_task['id']}", json={"priority": 1})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid fields"}
