"""Fixtures provide an isolated API and client for every test."""
from threading import Thread

import pytest

from api.client import APIClient
from demo_api.server import create_server


@pytest.fixture
def api_server():
    server = create_server()
    thread = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()


@pytest.fixture
def client(api_server):
    api_client = APIClient(api_server)
    yield api_client
    api_client.close()


@pytest.fixture
def task_payload():
    return {"title": "Learn API testing", "completed": False}


@pytest.fixture
def created_task(client, task_payload):
    response = client.request("POST", "/tasks", json=task_payload)
    assert response.status_code == 201, response.text
    return response.json()
