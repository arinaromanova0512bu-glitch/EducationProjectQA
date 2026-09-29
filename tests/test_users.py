import requests

from api_client import BASE_URL


def test_get_registered_user(registered_user):
    response = requests.get(f"{BASE_URL}/v1/users/{registered_user['id']}")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["user"]["id"] == registered_user["id"]
    assert response_data["user"]["email"] == registered_user["email"]
    assert response_data["user"]["name"] == registered_user["name"]
    assert response_data["user"]["role"] == "user"


def test_get_nonexistent_user():
    nonexistent_user_id = "00000000-0000-0000-0000-000000000000"

    response = requests.get(f"{BASE_URL}/v1/users/{nonexistent_user_id}")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"


def test_get_without_user_id():
    response = requests.get(f"{BASE_URL}/v1/users/")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["code"] == 3
    assert response_data["message"] == "user_id обязателен"


def test_delete_registered_user(registered_user):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }
    response = requests.delete(
        f"{BASE_URL}/v1/users/{registered_user['id']}",
        headers=headers
    )

    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/v1/users/{registered_user['id']}")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"


def test_delete_registered_user_without_token(registered_user):
    response = requests.delete(f"{BASE_URL}/v1/users/{registered_user['id']}")
    response_data = response.json()
    assert response.status_code == 401
    assert response_data["code"] == 16
    assert response_data["message"] == "требуется Authorization: Bearer <token>"


def test_delete_registered_user_with_invalid_token(registered_user):
    headers = {
        "Authorization": "Bearer invalid_token"
    }
    response = requests.delete(
        f"{BASE_URL}/v1/users/{registered_user['id']}",
        headers=headers
    )
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["code"] == 16
    assert response_data["message"] == "недействительный или просроченный токен"


def test_delete_user_with_mismatched_user_id(registered_user):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }
    nonexistent_user_id = "00000000-0000-0000-0000-000000000000"

    response = requests.delete(
        f"{BASE_URL}/v1/users/{nonexistent_user_id}",
        headers=headers
    )
    response_data = response.json()

    assert response.status_code == 403
    assert response_data["code"] == 7
    assert response_data["message"] == "user_id не совпадает с токеном"


def test_delete_registered_user_twice(registered_user):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }
    response = requests.delete(
        f"{BASE_URL}/v1/users/{registered_user['id']}",
        headers=headers
    )

    assert response.status_code == 200

    response = requests.delete(
        f"{BASE_URL}/v1/users/{registered_user['id']}",
        headers=headers
    )
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"
