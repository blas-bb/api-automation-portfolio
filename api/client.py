"""A small requests client shared by all tests."""
import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.trust_env = False  # Local tests do not need proxy settings.
        self.session.headers.update({"Authorization": "Bearer demo-token"})

    def request(self, method, path, **kwargs):
        return self.session.request(
            method, self.base_url + path, timeout=5, **kwargs
        )

    def close(self):
        self.session.close()
