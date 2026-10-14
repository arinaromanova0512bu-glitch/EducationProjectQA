from api_clients.base_http_client import BaseHttpClient
from config import BASE_URL


class UsersClient(BaseHttpClient):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL

    def get_user(self, user_id, **kwargs):
        response = self.get(
            f"/v1/users/{user_id}",
            **kwargs
        )
        return response

    def delete_user(self, user_id, **kwargs):
        response = self.delete(
            f"/v1/users/{user_id}",
            **kwargs
        )
        return response