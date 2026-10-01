from api_clients.base_http_client import BaseHttpClient
from config import BASE_URL


class OrderClient(BaseHttpClient):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL

    def create_order(self, user_id, **kwargs):
        data = {
            "user_id": user_id
        }

        response = self.post(
            "/v1/orders",
            json=data,
            **kwargs
        )
        return response

    def get_order(self, order_id, **kwargs):
        response = self.get(
            f"/v1/orders/{order_id}",
            **kwargs
        )
        return response

    def cancel_order(self, order_id, **kwargs):
        response = self.post(
            f"/v1/orders/{order_id}/cancel",
            **kwargs
        )
        return response

    def update_order_status(
            self,
            order_id,
            from_status,
            to_status,
            **kwargs
    ):
        data = {
            "from_status": from_status,
            "to_status": to_status
        }

        response = self.post(
            f"/v1/orders/{order_id}/status",
            json=data,
            **kwargs
        )

        return response
