def test_get_registered_user(registered_user, users_client):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }

    response = users_client.get_user(
        registered_user["id"],
        headers=headers
    )
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["user"]["id"] == registered_user["id"]
    assert response_data["user"]["email"] == registered_user["email"]
    assert response_data["user"]["name"] == registered_user["name"]
    assert response_data["user"]["role"] == "user"


def test_get_nonexistent_user(registered_user, users_client):
    nonexistent_user_id = "00000000-0000-0000-0000-000000000000"
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }

    response = users_client.get_user(
        nonexistent_user_id,
        headers=headers
    )
    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"


def test_get_without_user_id(users_client):
    response = users_client.get_user("")
    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 3
    assert response_data["message"] == "user_id обязателен"


def test_delete_registered_user(registered_user, users_client):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }

    response = users_client.delete_user(
        registered_user["id"],
        headers=headers
    )

    assert response.status_code == 200

    response = users_client.get_user(
        registered_user["id"],
        headers=headers
    )
    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"


def test_delete_registered_user_without_token(registered_user, users_client):
    response = users_client.delete_user(
        registered_user["id"]
    )
    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "требуется Authorization: Bearer <token>"


def test_delete_registered_user_with_invalid_token(registered_user, users_client):
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = users_client.delete_user(
        registered_user["id"],
        headers=headers
    )
    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "недействительный или просроченный токен"


def test_delete_user_with_mismatched_user_id(registered_user, users_client):
    nonexistent_user_id = "00000000-0000-0000-0000-000000000000"
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }

    response = users_client.delete_user(
        nonexistent_user_id,
        headers=headers
    )
    assert response.status_code == 403

    response_data = response.json()

    assert response_data["code"] == 7
    assert response_data["message"] == "user_id не совпадает с токеном"


def test_delete_registered_user_twice(registered_user, users_client):
    headers = {
        "Authorization": f"Bearer {registered_user['access_token']}"
    }
    response = users_client.delete_user(
        registered_user["id"],
        headers=headers
    )

    assert response.status_code == 200

    response = users_client.delete_user(
        registered_user["id"],
        headers=headers
    )
    response_data = response.json()

    assert response.status_code == 404
    assert response_data["code"] == 5
    assert response_data["message"] == "пользователь не найден"
