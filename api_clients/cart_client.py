from api_clients.base_http_client import BaseHttpClient
from config import BASE_URL


class CartClient(BaseHttpClient):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL

    def add_to_cart(self, user_id, product_id, quantity, **kwargs):
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        response = self.post(
            f"/v1/users/{user_id}/cart/items",
            json=data,
            **kwargs
        )
        return response

    def get_cart(self, user_id, **kwargs):
        response = self.get(
            f"/v1/users/{user_id}/cart",
            **kwargs
        )
        return response

    def remove_item(self, user_id, product_id, **kwargs):
        response = self.delete(
            f"/v1/users/{user_id}/cart/items/{product_id}",
            **kwargs
        )
        return response

    def clear_cart(self, user_id, **kwargs):
        response = self.delete(
            f"/v1/users/{user_id}/cart",
            **kwargs
        )
        return response

    def apply_promocode(self, user_id, code, **kwargs):
        data = {
            "code": code
        }
        response = self.post(
            f"/v1/users/{user_id}/cart/promocode",
            json=data,
            **kwargs
        )
        return response

    def clear_promocode(self, user_id, **kwargs):
        response = self.delete(
            f"/v1/users/{user_id}/cart/promocode",
            **kwargs
        )
        return response
