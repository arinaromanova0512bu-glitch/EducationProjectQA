import pytest
import requests
from faker import Faker

from api_client import BASE_URL


fake = Faker()


@pytest.fixture
def user_data():
    data = {"email": fake.email(),
            "password": "TestPassword123!",
            "name": fake.name()
            }
    return data


@pytest.fixture
def registered_user(user_data):
    response = requests.post(
        f"{BASE_URL}/v1/users/register",
        json=user_data
    )
    assert response.status_code == 200
    return user_data
