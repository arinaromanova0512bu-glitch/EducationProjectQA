import requests
import pytest

from api_client import BASE_URL


def test_user_registration_success(user_data):
    response = requests.post(f"{BASE_URL}/v1/users/register", json=user_data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["user"]["email"] == user_data["email"]
    assert response_data["user"]["name"] == user_data["name"]
    assert "id" in response_data["user"]
    assert response_data["user"]["role"] == "user"
    assert response_data["accessToken"]


def test_user_login_success(registered_user):
    login_data = {
        "email":registered_user["email"],
        "password":registered_user["password"]
    }

    response=requests.post(f"{BASE_URL}/v1/users/login", json=login_data)
    response_data=response.json()

    assert response.status_code == 200
    assert response_data["user"]["email"] == registered_user["email"]
    assert response_data["accessToken"]


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("password", "WrongPassword123!"),
        ("email", "unknown@example.com")
    ]
)
def test_user_login_with_invalid_credentials(
        registered_user, field, invalid_value
):
    login_data = {
        "email":registered_user["email"],
        "password":registered_user["password"]
    }
    login_data[field] = invalid_value

    response = requests.post(f"{BASE_URL}/v1/users/login", json=login_data)
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["code"] == 16
    assert response_data["message"] == "неверный email или пароль"


@pytest.mark.parametrize(
    "field, action",
    [
        ("email", "empty"),
        ("email","remove"),
        ("password", "empty"),
        ("password", "remove")
    ]
)
def test_user_login_with_missing_or_empty_required_field(
        registered_user, field, action
):
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }

    if action == "empty":
        login_data[field] = ""
    elif action == "remove":
        login_data.pop(field)

    response = requests.post(f"{BASE_URL}/v1/users/login", json=login_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert response_data["message"] == "email и password обязательны"


@pytest.mark.parametrize(
    "field",
    ["email","password"]
)
def test_user_login_with_invalid_field_type(registered_user, field):
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    login_data[field] = 123

    response = requests.post(f"{BASE_URL}/v1/users/login", json=login_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert f"invalid value for string field {field}" in response_data["message"]


@pytest.mark.parametrize(
    "field, action",
    [
        ("email", "empty"),
        ("email", "remove"),
        ("password", "empty"),
        ("password", "remove")
    ]
)
def test_user_registration_with_missing_or_empty_required_field(
        user_data, field, action
):
    if action == "empty":
        user_data[field] = ""
    elif action == "remove":
        user_data.pop(field)

    response = requests.post(f"{BASE_URL}/v1/users/register", json=user_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert response_data["message"] == "email и password обязательны"


@pytest.mark.parametrize(
    "field",
    ["email", "password", "name"])
def test_user_registration_with_invalid_field_type(user_data, field):
    user_data[field] = 123

    response = requests.post(f"{BASE_URL}/v1/users/register", json=user_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert f"invalid value for string field {field}" in response_data["message"]

def test_user_registration_with_whitespace_only_email(user_data):
    user_data["email"] = "    "

    response = requests.post(f"{BASE_URL}/v1/users/register", json=user_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert response_data["message"] == "email и password обязательны"

