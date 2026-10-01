from api_clients.base_http_client import BaseHttpClient
from config import BASE_URL


class CatalogClient(BaseHttpClient):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL

    def get_products(self):
        response = self.get("/v1/products")
        return response

    def get_product(self, product_id):
        response = self.get(f"/v1/products/{product_id}")
        return response



