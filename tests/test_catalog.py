def test_get_products_list(catalog_client):
    response = catalog_client.get_products()

    assert response.status_code == 200

    response_data = response.json()

    assert "products" in response_data
    assert "nextPageToken" in response_data
    assert isinstance(response_data["products"], list)


def test_product_structure_in_products_list(catalog_client):
    response = catalog_client.get_products()

    assert response.status_code == 200

    response_data = response.json()
    product = response_data["products"][0]

    assert "id" in product
    assert "name" in product
    assert "description" in product
    assert "priceCents" in product
    assert "stockQuantity" in product
    assert "brand" in product


def test_get_existing_product(products, catalog_client):
    product_id = products[0]["id"]

    response = catalog_client.get_product(product_id)

    assert response.status_code == 200

    product_response_data = response.json()

    assert product_id == product_response_data["product"]["id"]


def test_get_nonexistent_product(catalog_client):
    product_id = "00000000-0000-0000-0000-000000000000"

    response = catalog_client.get_product(product_id)

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["code"] == 5
    assert response_data["message"] == f"Товар с ID '{product_id}' не найден"


def test_get_product_with_empty_product_id(catalog_client):
    product_id = ""

    response = catalog_client.get_product(product_id)

    assert response.status_code == 400

    response_data = response.json()

    assert response_data["code"] == 3
    assert response_data["message"] == "ID товара не может быть пустым"

