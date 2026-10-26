def test_create_order(
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
    price_cents = product["priceCents"]
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

    response_data = response.json()
    order = response_data["order"]

    assert order["userId"] == user_id
    assert order["status"] == "ORDER_STATUS_CREATED"
    assert len(order["items"]) == 1

    order_item = order["items"][0]

    assert order_item["productId"] == product_id
    assert order_item["quantity"] == quantity
    assert int(order_item["priceCents"]) == int(price_cents)

    expected_total = int(price_cents) * quantity

    assert int(order["totalAmountCents"]) == expected_total


def test_create_order_with_multiple_products(
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
    second_product = products[1]

    product_id = product["id"]
    second_product_id = second_product["id"]

    price_cents = product["priceCents"]
    second_price_cents = second_product["priceCents"]

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
        second_product_id,
        second_quantity,
        headers=headers
    )

    assert response.status_code == 200

    response = order_client.create_order(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()
    order = response_data["order"]

    assert order["userId"] == user_id
    assert order["status"] == "ORDER_STATUS_CREATED"
    assert len(order["items"]) == 2

    first_order_item = next(
        item for item in order["items"]
        if item["productId"] == product_id
    )

    second_order_item = next(
        item for item in order["items"]
        if item["productId"] == second_product_id
    )

    assert first_order_item["productId"] == product_id
    assert first_order_item["quantity"] == quantity
    assert int(first_order_item["priceCents"]) == int(price_cents)

    assert second_order_item["productId"] == second_product_id
    assert second_order_item["quantity"] == second_quantity
    assert int(second_order_item["priceCents"]) == int(second_price_cents)

    expected_total = (
        int(price_cents) * quantity
        + int(second_price_cents) * second_quantity
    )

    assert int(order["totalAmountCents"]) == expected_total


def test_cart_is_cleared_after_order_creation(
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

    response = cart_client.get_cart(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data["items"]) == 0


def test_create_order_with_empty_user_id(
        registered_user,
        order_client
):
    user_id = ""
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = order_client.create_order(
        user_id,
        headers=headers
    )

    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 3
    assert response_data["message"] == "user_id обязателен"


def test_create_order_without_token(
        registered_user,
        order_client
):
    user_id = registered_user["id"]

    response = order_client.create_order(
        user_id
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "требуется Authorization: Bearer <token>"


def test_create_order_with_invalid_token(
        registered_user,
        order_client
):
    user_id = registered_user["id"]
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = order_client.create_order(
        user_id,
        headers=headers
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "недействительный или просроченный токен"


def test_create_order_with_another_user_token(
        registered_user,
        order_client,
        second_registered_user
):
    user_id = registered_user["id"]
    second_access_token = second_registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {second_access_token}"
    }

    response = order_client.create_order(
        user_id,
        headers=headers
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["code"] == 7
    assert response_data["message"] == "user_id не совпадает с токеном"


def test_get_order_by_owner(
        created_order,
        order_client
):
    order_id = created_order["order_id"]
    user_id = created_order["user_id"]
    headers = created_order["headers"]

    response = order_client.get_order(
        order_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["order"]["id"] == order_id
    assert response_data["order"]["userId"] == user_id


def test_get_nonexistent_order(
        registered_user,
        order_client
):
    access_token = registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    order_id = "00000000-0000-0000-0000-000000000000"

    response = order_client.get_order(
        order_id,
        headers=headers
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == "заказ не найден"


def test_get_order_by_another_user(
        created_order,
        second_registered_user,
        order_client
):
    order_id = created_order["order_id"]

    second_access_token = second_registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {second_access_token}"
    }

    response = order_client.get_order(
        order_id,
        headers=headers
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["code"] == 7
    assert response_data["message"] == "нет доступа к заказу"


def test_cancel_order(
        created_order,
        order_client
):
    order_id = created_order["order_id"]
    user_id = created_order["user_id"]
    headers = created_order["headers"]

    response = order_client.cancel_order(
        order_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()
    order = response_data["order"]

    assert order["id"] == order_id
    assert order["userId"] == user_id
    assert order["status"] == "ORDER_STATUS_CANCELLED"
    assert len(order["items"]) == 1


def test_update_order_status_from_created_to_paid(
        created_order,
        order_client
):
    order_id = created_order["order_id"]
    user_id = created_order["user_id"]
    headers = created_order["headers"]

    response = order_client.update_order_status(
        order_id,
        "ORDER_STATUS_CREATED",
        "ORDER_STATUS_PAID",
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()
    order = response_data["order"]

    assert order["id"] == order_id
    assert order["userId"] == user_id
    assert order["status"] == "ORDER_STATUS_PAID"


def test_update_order_status_with_invalid_transition(
        created_order,
        order_client
):
    order_id = created_order["order_id"]
    headers = created_order["headers"]

    response = order_client.update_order_status(
        order_id,
        "ORDER_STATUS_CREATED",
        "ORDER_STATUS_SHIPPED",
        headers=headers
    )

    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 9
    assert response_data["message"] == "недопустимый переход статуса"


def test_update_order_status_with_wrong_from_status(
        created_order,
        order_client
):
    order_id = created_order["order_id"]
    headers = created_order["headers"]

    response = order_client.update_order_status(
        order_id,
        "ORDER_STATUS_PAID",
        "ORDER_STATUS_SHIPPED",
        headers=headers
    )

    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 9
    assert response_data["message"] == "текущий статус не совпадает с from_status"