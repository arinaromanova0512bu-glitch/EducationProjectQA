from api_clients.base_http_client import BaseHttpClient
from config import BASE_URL


class AuthClient(BaseHttpClient):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL

    def register_user(self, data):
        response = self.post(
            "/v1/users/register",
            json=data
        )

        return response

    def login_user(self, data):
        response = self.post(
            "/v1/users/login",
            json=data
        )

        return response

