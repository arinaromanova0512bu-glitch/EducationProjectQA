import logging

from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_add_product_to_cart(empty_cart, cart_page):
    logger.info("Начинаем тест добавления товара в корзину")

    first_product = empty_cart.product_cards.first
    product_name = first_product.get_by_test_id("product-name").inner_text()

    logger.info("Добавляем товар в корзину")

    empty_cart.add_to_cart()

    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_items.first).to_be_visible()
    expect(cart_page.cart_item_names.first).to_have_text(product_name)
    expect(cart_page.cart_item_quantities.first).to_have_text("1")


def test_cart_displays_product(empty_cart, cart_page):
    logger.info("Начинаем тест отображения товара")

    first_product = empty_cart.product_cards.first
    product_name = first_product.get_by_test_id("product-name").inner_text()
    product_price = first_product.get_by_test_id("product-price").inner_text()

    logger.info("Добавляем товар в корзину")

    empty_cart.add_to_cart()

    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_item_names.first).to_have_text(product_name)
    expect(cart_page.cart_item_line_totals.first).to_have_text(product_price)
    expect(cart_page.cart_item_quantities.first).to_have_text("1")
    expect(cart_page.cart_item_brands.first).to_be_visible()


def test_add_multiple_products(empty_cart, cart_page):
    logger.info("Начинаем тест добавления нескольких товаров")

    first_product = empty_cart.product_cards.nth(0)
    second_product = empty_cart.product_cards.nth(1)
    first_product_name = first_product.get_by_test_id("product-name").inner_text()
    second_product_name = second_product.get_by_test_id("product-name").inner_text()

    logger.info("Добавляем товары в корзину")

    empty_cart.add_to_cart()
    empty_cart.add_to_cart(1)

    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_item_names.nth(0)).to_have_text(first_product_name)
    expect(cart_page.cart_item_names.nth(1)).to_have_text(second_product_name)
    expect(cart_page.cart_items).to_have_count(2)
    expect(cart_page.cart_item_quantities.nth(0)).to_have_text("1")
    expect(cart_page.cart_item_quantities.nth(1)).to_have_text("1")


def test_remove_product_from_cart(empty_cart, cart_page):
    logger.info("Начинаем тест удаления товара из корзины")
    logger.info("Добавляем товары в корзину")

    empty_cart.add_to_cart()
    empty_cart.add_to_cart(1)

    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_items).to_have_count(2)

    remaining_product_name = cart_page.cart_item_names.nth(1).inner_text()

    logger.info("Удаляем первый товар")

    cart_page.remove_item()

    expect(cart_page.cart_items).to_have_count(1)
    expect(cart_page.cart_item_quantities.nth(0)).to_have_text("1")
    expect(cart_page.cart_item_names.first).to_have_text(remaining_product_name)


def test_clear_cart(empty_cart, cart_page):
    logger.info("Начинаем тест удаления всех товаров из корзины")
    logger.info("Добавляем товары в корзину")

    empty_cart.add_to_cart()
    empty_cart.add_to_cart(1)

    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_items).to_have_count(2)

    cart_page.clear_cart()

    expect(cart_page.cart_items).to_have_count(0)


def test_cart_total_price(empty_cart, cart_page):
    logger.info("Начинаем тест проверки общей стоимости")

    first_product = empty_cart.product_cards.nth(0)
    second_product = empty_cart.product_cards.nth(1)
    first_product_price = int(
        first_product.get_by_test_id("product-price").get_attribute("data-price-cents")
    )
    second_product_price = int(
        second_product.get_by_test_id("product-price").get_attribute("data-price-cents")
    )

    logger.info("Добавляем товары в корзину")

    empty_cart.add_to_cart()
    empty_cart.add_to_cart(1)

    logger.info("Переходим в корзину")

    cart_page.open_cart()
    cart_page.remove_promo()

    expected_total = first_product_price + second_product_price
    actual_total = int(cart_page.cart_total.get_attribute("data-cents"))

    assert expected_total == actual_total


def test_apply_invalid_promo(add_to_cart, cart_page):
    logger.info("Начинаем тест применения неправильного промокода")
    logger.info("Переходим в корзину")

    cart_page.open_cart()
    cart_page.remove_promo()
    expect(cart_page.cart_discount).to_have_attribute("data-cents", "0")

    total_before = int(cart_page.cart_total.get_attribute("data-cents"))

    cart_page.apply_promo("INVALID123")

    total_after = int(cart_page.cart_total.get_attribute("data-cents"))

    assert total_before == total_after
    expect(cart_page.cart_discount).to_have_attribute("data-cents", "0")


def test_apply_valid_promo(add_to_cart, cart_page):
    logger.info("Начинаем тест применения правильного промокода")
    logger.info("Переходим в корзину")

    cart_page.open_cart()

    cart_page.remove_promo()
    expect(cart_page.cart_item_names.first).to_be_visible()
    expect(cart_page.cart_discount).to_have_attribute("data-cents", "0")

    total_before = int(cart_page.cart_total.get_attribute("data-cents"))

    cart_page.apply_promo("SAVE10")

    expected_discount = total_before * 10 // 100

    expect(cart_page.cart_discount).to_have_attribute(
        "data-cents",
        str(expected_discount)
    )

    total_after = int(cart_page.cart_total.get_attribute("data-cents"))

    assert total_before > total_after


def test_empty_cart(add_to_cart, cart_page):
    logger.info("Начинаем тест пустой корзины")
    logger.info("Переходим в корзину")

    cart_page.open_cart()

    expect(cart_page.cart_items.first).to_be_visible()

    cart_page.clear_cart()

    expect(cart_page.cart_items).to_have_count(0)
    expect(cart_page.cart_empty).to_be_visible()
    actual_total = int(cart_page.cart_total.get_attribute("data-cents"))

    assert actual_total == 0

    actual_discount = int(cart_page.cart_discount.get_attribute("data-cents"))

    assert actual_discount == 0