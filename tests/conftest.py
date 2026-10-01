import pytest
from faker import Faker

from api_clients.auth_client import AuthClient
from api_clients.users_client import UsersClient
from api_clients.catalog_client import CatalogClient
from api_clients.cart_client import CartClient
from api_clients.order_client import OrderClient

fake = Faker()


@pytest.fixture
def auth_client():
    return AuthClient()


@pytest.fixture
def users_client():
    return UsersClient()


@pytest.fixture
def catalog_client():
    return CatalogClient()


@pytest.fixture
def cart_client():
    return CartClient()


@pytest.fixture
def order_client():
    return OrderClient()


@pytest.fixture
def user_data():
    data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return data


@pytest.fixture
def registered_user(user_data, auth_client):
    response = auth_client.register_user(user_data)

    assert response.status_code == 200

    response_data = response.json()

    registered_user_data = {
        "id": response_data["user"]["id"],
        "email": response_data["user"]["email"],
        "name": response_data["user"]["name"],
        "password": user_data["password"],
        "access_token": response_data["accessToken"]
    }

    return registered_user_data


@pytest.fixture
def products(catalog_client):
    response = catalog_client.get_products()

    assert response.status_code == 200

    response_data = response.json()

    return response_data["products"]


@pytest.fixture
def second_registered_user(auth_client):
    data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }

    response = auth_client.register_user(data)

    assert response.status_code == 200

    response_data = response.json()

    return {
        "id": response_data["user"]["id"],
        "email": response_data["user"]["email"],
        "name": response_data["user"]["name"],
        "password": data["password"],
        "access_token": response_data["accessToken"]
    }


@pytest.fixture
def created_order(
        registered_user,
        products,
        cart_client,
        order_client
):
    user_id = registered_user["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    product = products[0]
    product_id = product["id"]
    quantity = 2

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response = order_client.create_order(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    order = response.json()["order"]

    return {
        "order": order,
        "order_id": order["id"],
        "user_id": user_id,
        "headers": headers
    }
