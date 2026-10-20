import logging

import allure
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


@allure.epic("Интернет-магазин")
@allure.feature("Корзина")
@allure.story("Управление товарами в корзине")
class TestCartProducts:

    @allure.title("Добавление товара в корзину")
    def test_add_product_to_cart(self, empty_cart, cart_page):
        logger.info("Начинаем тест добавления товара в корзину")

        with allure.step("Получить название первого товара"):
            first_product = empty_cart.product_cards.first
            product_name = first_product.get_by_test_id(
                "product-name"
            ).inner_text()

        logger.info("Добавляем товар в корзину")

        with allure.step("Добавить первый товар в корзину"):
            empty_cart.add_to_cart()

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить наличие товара и его количество"):
            expect(cart_page.cart_items.first).to_be_visible()
            expect(cart_page.cart_item_names.first).to_have_text(product_name)
            expect(cart_page.cart_item_quantities.first).to_have_text("1")

    @allure.title("Отображение информации о товаре в корзине")
    def test_cart_displays_product(self, empty_cart, cart_page):
        logger.info("Начинаем тест отображения товара")

        with allure.step("Получить название и стоимость первого товара"):
            first_product = empty_cart.product_cards.first
            product_name = first_product.get_by_test_id(
                "product-name"
            ).inner_text()
            product_price = first_product.get_by_test_id(
                "product-price"
            ).inner_text()

        logger.info("Добавляем товар в корзину")

        with allure.step("Добавить товар в корзину"):
            empty_cart.add_to_cart()

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить информацию о товаре"):
            expect(cart_page.cart_item_names.first).to_have_text(product_name)
            expect(cart_page.cart_item_line_totals.first).to_have_text(
                product_price
            )
            expect(cart_page.cart_item_quantities.first).to_have_text("1")
            expect(cart_page.cart_item_brands.first).to_be_visible()

    @allure.title("Добавление нескольких товаров в корзину")
    def test_add_multiple_products(self, empty_cart, cart_page):
        logger.info("Начинаем тест добавления нескольких товаров")

        with allure.step("Получить названия двух товаров"):
            first_product = empty_cart.product_cards.nth(0)
            second_product = empty_cart.product_cards.nth(1)

            first_product_name = first_product.get_by_test_id(
                "product-name"
            ).inner_text()
            second_product_name = second_product.get_by_test_id(
                "product-name"
            ).inner_text()

        logger.info("Добавляем товары в корзину")

        with allure.step("Добавить два товара в корзину"):
            empty_cart.add_to_cart()
            empty_cart.add_to_cart(1)

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить отображение двух товаров"):
            expect(cart_page.cart_items).to_have_count(2)

            actual_names = cart_page.cart_item_names.all_inner_texts()

            assert set(actual_names) == {
                first_product_name,
                second_product_name
            }

            expect(cart_page.cart_item_quantities.nth(0)).to_have_text("1")
            expect(cart_page.cart_item_quantities.nth(1)).to_have_text("1")

    @allure.title("Удаление одного товара из корзины")
    def test_remove_product_from_cart(self, empty_cart, cart_page):
        logger.info("Начинаем тест удаления товара из корзины")
        logger.info("Добавляем товары в корзину")

        with allure.step("Добавить два товара в корзину"):
            empty_cart.add_to_cart()
            empty_cart.add_to_cart(1)

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить наличие двух товаров"):
            expect(cart_page.cart_items).to_have_count(2)

        with allure.step("Сохранить название второго товара"):
            remaining_product_name = cart_page.cart_item_names.nth(
                1
            ).inner_text()

        logger.info("Удаляем первый товар")

        with allure.step("Удалить первый товар"):
            cart_page.remove_item()

        with allure.step("Проверить, что в корзине остался второй товар"):
            expect(cart_page.cart_items).to_have_count(1)
            expect(cart_page.cart_item_quantities.nth(0)).to_have_text("1")
            expect(cart_page.cart_item_names.first).to_have_text(
                remaining_product_name
            )

    @allure.title("Очистка корзины")
    def test_clear_cart(self, empty_cart, cart_page):
        logger.info("Начинаем тест удаления всех товаров из корзины")
        logger.info("Добавляем товары в корзину")

        with allure.step("Добавить два товара в корзину"):
            empty_cart.add_to_cart()
            empty_cart.add_to_cart(1)

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить наличие двух товаров"):
            expect(cart_page.cart_items).to_have_count(2)

        with allure.step("Очистить корзину"):
            cart_page.clear_cart()

        with allure.step("Проверить отсутствие товаров"):
            expect(cart_page.cart_items).to_have_count(0)

    @allure.title("Отображение пустой корзины")
    def test_empty_cart(self, add_to_cart, cart_page):
        logger.info("Начинаем тест пустой корзины")
        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Проверить наличие товара"):
            expect(cart_page.cart_items.first).to_be_visible()

        with allure.step("Удалить все товары"):
            cart_page.clear_cart()

        with allure.step("Проверить отображение пустой корзины"):
            expect(cart_page.cart_items).to_have_count(0)
            expect(cart_page.cart_empty).to_be_visible()

        with allure.step("Проверить нулевую стоимость корзины"):
            actual_total = int(
                cart_page.cart_total.get_attribute("data-cents")
            )
            assert actual_total == 0

        with allure.step("Проверить отсутствие скидки"):
            actual_discount = int(
                cart_page.cart_discount.get_attribute("data-cents")
            )
            assert actual_discount == 0


@allure.epic("Интернет-магазин")
@allure.feature("Корзина")
@allure.story("Расчёт стоимости корзины")
class TestCartTotal:

    @allure.title("Расчёт общей стоимости товаров в корзине")
    def test_cart_total_price(self, empty_cart, cart_page):
        logger.info("Начинаем тест проверки общей стоимости")

        with allure.step("Получить стоимость двух товаров"):
            first_product = empty_cart.product_cards.nth(0)
            second_product = empty_cart.product_cards.nth(1)

            first_product_price = int(
                first_product.get_by_test_id(
                    "product-price"
                ).get_attribute("data-price-cents")
            )
            second_product_price = int(
                second_product.get_by_test_id(
                    "product-price"
                ).get_attribute("data-price-cents")
            )

        logger.info("Добавляем товары в корзину")

        with allure.step("Добавить два товара в корзину"):
            empty_cart.add_to_cart()
            empty_cart.add_to_cart(1)

        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину и удалить промокод"):
            cart_page.open_cart()
            cart_page.remove_promo()

        with allure.step("Рассчитать ожидаемую общую стоимость"):
            expected_total = first_product_price + second_product_price

        with allure.step("Получить фактическую стоимость корзины"):
            actual_total = int(
                cart_page.cart_total.get_attribute("data-cents")
            )

        with allure.step("Сравнить ожидаемую и фактическую стоимость"):
            assert expected_total == actual_total


@allure.epic("Интернет-магазин")
@allure.feature("Корзина")
@allure.story("Применение промокодов")
class TestCartPromo:

    @allure.title("Неверный промокод не изменяет стоимость корзины")
    def test_apply_invalid_promo(self, add_to_cart, cart_page):
        logger.info("Начинаем тест применения неправильного промокода")
        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Удалить промокод и проверить отсутствие скидки"):
            cart_page.remove_promo()
            expect(cart_page.cart_discount).to_have_attribute(
                "data-cents", "0"
            )

        with allure.step("Получить стоимость корзины до промокода"):
            total_before = int(
                cart_page.cart_total.get_attribute("data-cents")
            )

        with allure.step("Применить неверный промокод"):
            cart_page.apply_promo("INVALID123")

        with allure.step("Получить стоимость корзины после промокода"):
            total_after = int(
                cart_page.cart_total.get_attribute("data-cents")
            )

        with allure.step("Проверить отсутствие изменений стоимости и скидки"):
            assert total_before == total_after
            expect(cart_page.cart_discount).to_have_attribute(
                "data-cents", "0"
            )

    @allure.title("Корректный промокод применяет скидку 10%")
    def test_apply_valid_promo(self, add_to_cart, cart_page):
        logger.info("Начинаем тест применения правильного промокода")
        logger.info("Переходим в корзину")

        with allure.step("Открыть корзину"):
            cart_page.open_cart()

        with allure.step("Удалить промокод и проверить отсутствие скидки"):
            cart_page.remove_promo()
            expect(cart_page.cart_item_names.first).to_be_visible()
            expect(cart_page.cart_discount).to_have_attribute(
                "data-cents", "0"
            )

        with allure.step("Получить стоимость корзины до скидки"):
            total_before = int(
                cart_page.cart_total.get_attribute("data-cents")
            )

        with allure.step("Применить промокод SAVE10"):
            cart_page.apply_promo("SAVE10")

        with allure.step("Рассчитать ожидаемую скидку 10%"):
            expected_discount = total_before * 10 // 100

        with allure.step("Проверить размер скидки"):
            expect(cart_page.cart_discount).to_have_attribute(
                "data-cents",
                str(expected_discount)
            )

        with allure.step("Получить стоимость после применения скидки"):
            total_after = int(
                cart_page.cart_total.get_attribute("data-cents")
            )

        with allure.step("Проверить уменьшение общей стоимости"):
            assert total_before > total_after