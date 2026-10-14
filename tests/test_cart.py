def test_add_item_to_cart(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 2

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"][0]["productId"] == product_id
    assert response_data["items"][0]["quantity"] == quantity
    assert len(response_data["items"]) == 1
    assert int(response_data["totalPriceCents"]) > 0


def test_get_cart_with_item(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 2

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"][0]["productId"] == product_id


def test_add_item_updates_quantity(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 2
    second_quantity = 5

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        second_quantity,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"][0]["quantity"] == second_quantity
    assert len(response_data["items"]) == 1


def test_add_item_with_quantity_1(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 1

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"][0]["productId"] == product_id
    assert response_data["items"][0]["quantity"] == quantity
    assert len(response_data["items"]) == 1


def test_add_item_with_quantity_99(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 99

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"][0]["productId"] == product_id
    assert response_data["items"][0]["quantity"] == quantity
    assert len(response_data["items"]) == 1


def test_add_item_with_zero_quantity(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 0

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 3
    assert response_data["message"] == "quantity must be greater than zero"


def test_add_item_with_quantity_100(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 100

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )
    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 3
    assert response_data["message"] == "max 99 items per product allowed"


def test_add_nonexistent_product(registered_user, cart_client):
    user_id = registered_user["id"]
    product_id = "00000000-0000-0000-0000-000000000000"
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 1

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == "товар не найден в каталоге"


def test_remove_item_from_cart(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 2

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response = cart_client.remove_item(
        user_id,
        product_id,
        headers=headers
    )

    assert response.status_code == 200

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"] == []


def test_clear_cart(registered_user, products, cart_client):
    user_id = registered_user["id"]
    product_id = products[0]["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    quantity = 2

    response = cart_client.add_to_cart(
        user_id,
        product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    second_product_id = products[1]["id"]

    response = cart_client.add_to_cart(
        user_id,
        second_product_id,
        quantity,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data["items"]) == 2

    response = cart_client.clear_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["items"] == []


def test_get_empty_cart(registered_user, cart_client):
    user_id = registered_user["id"]
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data["items"]) == 0


def test_cart_without_token(registered_user, cart_client):
    user_id = registered_user["id"]

    response = cart_client.get_cart(
        user_id
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "требуется Authorization: Bearer <token>"


def test_cart_with_invalid_token(registered_user, cart_client):
    user_id = registered_user["id"]
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "недействительный или просроченный токен"


def test_cart_with_another_user_token(
        registered_user,
        cart_client,
        second_registered_user
):
    user_id = registered_user["id"]
    second_access_token = second_registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {second_access_token}"
    }

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["code"] == 7
    assert response_data["message"] == "user_id не совпадает с токеном"

