import pytest


@pytest.mark.parametrize("method,path", [("GET", "/tasks"), ("POST", "/tasks"), ("PUT", "/tasks/1"), ("PATCH", "/tasks/1"), ("DELETE", "/tasks/1")])
@pytest.mark.parametrize("token", [None, "Bearer wrong-token"])
def test_reject_unauthorized_requests(client, method, path, token):
    client.session.headers.pop("Authorization")
    if token is not None:
        client.session.headers["Authorization"] = token
    response = client.request(method, path)
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}
