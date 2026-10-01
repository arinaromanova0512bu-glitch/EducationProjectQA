def test_apply_percent_promocode(
        registered_user,
        products,
        cart_client
):
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

    code = "SAVE10"

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["appliedPromocode"] == code

    expected_discount = int(response_data["subtotalCents"]) * 10 // 100
    expected_total = int(response_data["subtotalCents"]) - expected_discount
    expected_subtotal = int(products[0]["priceCents"]) * quantity

    assert int(response_data["discountCents"]) == expected_discount
    assert int(response_data["totalPriceCents"]) == expected_total
    assert int(response_data["subtotalCents"]) == expected_subtotal


def test_apply_fixed_promocode(
        registered_user,
        products,
        cart_client
):
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

    code = "FLAT500"

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["appliedPromocode"] == code

    expected_discount = 500
    expected_subtotal = int(products[0]["priceCents"]) * quantity
    expected_total = expected_subtotal - expected_discount

    assert int(response_data["subtotalCents"]) == expected_subtotal
    assert int(response_data["discountCents"]) == expected_discount
    assert int(response_data["totalPriceCents"]) == expected_total


def test_clear_promocode(
        registered_user,
        products,
        cart_client
):
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

    code = "SAVE10"

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=headers
    )

    assert response.status_code == 200

    response = cart_client.clear_promocode(
        user_id,
        headers=headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["appliedPromocode"] == ""

    expected_total = int(products[0]["priceCents"]) * quantity

    assert int(response_data["discountCents"]) == 0
    assert int(response_data["totalPriceCents"]) == expected_total


def test_apply_nonexistent_promocode(
        registered_user,
        products,
        cart_client
):
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

    code = "NOTEXIST"

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=headers
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == "промокод не найден"


def test_apply_promocode_without_token(
        registered_user,
        products,
        cart_client
):
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

    code = "SAVE10"

    response = cart_client.apply_promocode(
        user_id,
        code
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "требуется Authorization: Bearer <token>"


def test_apply_promocode_with_invalid_token(
        registered_user,
        products,
        cart_client
):
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

    code = "SAVE10"
    invalid_headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=invalid_headers
    )

    assert response.status_code == 401

    response_data = response.json()

    assert response_data["code"] == 16
    assert response_data["message"] == "недействительный или просроченный токен"


def test_apply_promocode_with_another_user_token(
        registered_user,
        second_registered_user,
        products,
        cart_client
):
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

    code = "SAVE10"
    second_access_token = second_registered_user["access_token"]
    headers = {
        "Authorization": f"Bearer {second_access_token}"
    }

    response = cart_client.apply_promocode(
        user_id,
        code,
        headers=headers
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["code"] == 7
    assert response_data["message"] == "user_id не совпадает с токеном"


