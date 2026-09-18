def test_delete_task(client, created_task):
    path = f"/tasks/{created_task['id']}"
    response = client.request("DELETE", path)
    assert response.status_code == 204
    assert response.content == b""
    missing = client.request("GET", path)
    assert missing.status_code == 404
    assert missing.json() == {"error": "Task not found"}


def test_delete_missing_task(client):
    response = client.request("DELETE", "/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found"}


def test_delete_twice(client, created_task):
    path = f"/tasks/{created_task['id']}"
    assert client.request("DELETE", path).status_code == 204
    response = client.request("DELETE", path)
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found"}
