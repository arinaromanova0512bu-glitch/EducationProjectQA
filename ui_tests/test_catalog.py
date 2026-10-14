import logging

import allure
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


@allure.epic("Интернет-магазин")
@allure.feature("Каталог")
@allure.story("Отображение и поиск товаров")
class TestCatalogProducts:

    @allure.title("Отображение товаров в каталоге")
    def test_catalog_displays_products(self, logged_in_catalog):
        logger.info("Начинаем тест отображения товаров")

        catalog_page = logged_in_catalog

        logger.info("Проверяем отображение товаров в каталоге")

        with allure.step("Проверить отображение товаров в каталоге"):
            expect(catalog_page.product_cards.first).to_be_visible()

    @allure.title("Поиск товаров в каталоге")
    def test_catalog_search(self, logged_in_catalog):
        logger.info("Начинаем тест поиска товаров")

        catalog_page = logged_in_catalog

        with allure.step("Выполнить поиск товара iPhone"):
            catalog_page.search("iPhone")

        logger.info("Проверяем результат поиска")

        with allure.step("Дождаться отображения товаров iPhone"):
            catalog_page.page.wait_for_function(
                """() => {
                    const cards = document.querySelectorAll(
                        '[data-testid="product-card"]'
                    );

                    return cards.length > 0 &&
                        Array.from(cards).every(card => {
                            const name = card.querySelector(
                                '[data-testid="product-name"]'
                            );

                            return name &&
                                name.textContent.toLowerCase().includes('iphone');
                        });
                }"""
            )

        with allure.step("Получить количество найденных товаров"):
            cards_count = catalog_page.product_cards.count()

        logger.info(f"Количество найденных товаров: {cards_count}")

        with allure.step("Проверить, что товары найдены"):
            assert cards_count > 0


@allure.epic("Интернет-магазин")
@allure.feature("Каталог")
@allure.story("Фильтрация товаров")
class TestCatalogFilters:

    @allure.title("Фильтрация товаров по категории")
    def test_catalog_category_filter(self, logged_in_catalog):
        logger.info("Начинаем тест фильтрации по категории")

        catalog_page = logged_in_catalog

        with allure.step("Выбрать категорию смартфонов"):
            catalog_page.select_smartphones()

        with allure.step("Проверить активность фильтра смартфонов"):
            expect(catalog_page.smartphones_filter).to_have_attribute(
                "data-active", "true"
            )

        with allure.step("Получить идентификатор категории"):
            category_id = catalog_page.smartphones_filter.get_attribute(
                "data-category-id"
            )

            assert category_id is not None

        with allure.step("Дождаться фильтрации товаров по категории"):
            catalog_page.page.wait_for_function(
                """(categoryId) => {
                    const cards = document.querySelectorAll(
                        '[data-testid="product-card"]'
                    );
                    return cards.length > 0 &&
                        Array.from(cards).every(card =>
                            card.getAttribute('data-category-id') === categoryId
                        );
                }""",
                arg=category_id
            )

        with allure.step("Получить количество смартфонов"):
            cards_count = catalog_page.product_cards.count()

        logger.info(f"Количество смартфонов: {cards_count}")

        with allure.step("Проверить наличие товаров"):
            assert cards_count > 0

        with allure.step("Проверить категорию каждого товара"):
            for i in range(cards_count):
                product_card = catalog_page.product_cards.nth(i)
                product_category = product_card.get_attribute(
                    "data-category-id"
                )
                logger.info(
                    f"Товар {i}: категория {product_category}"
                )
                assert product_category == category_id

    @allure.title("Фильтрация товаров по бренду")
    def test_catalog_brand_filter(self, logged_in_catalog):
        logger.info("Начинаем тест фильтрации по бренду")

        catalog_page = logged_in_catalog

        with allure.step("Выбрать бренд Apple"):
            catalog_page.select_brand()

        with allure.step("Проверить активность фильтра бренда"):
            expect(catalog_page.brand_filter).to_have_attribute(
                "data-active", "true"
            )

        with allure.step("Дождаться отображения товаров Apple"):
            catalog_page.page.wait_for_function(
                """() => {
                    const cards = document.querySelectorAll(
                        '[data-testid="product-card"]'
                    );
                    return cards.length > 0 &&
                        Array.from(cards).every(card =>
                            card.getAttribute('data-brand') === 'apple'
                        );
                }"""
            )

        with allure.step("Получить количество товаров Apple"):
            cards_count = catalog_page.product_cards.count()

        logger.info(f"Количество товаров Apple: {cards_count}")

        with allure.step("Проверить наличие товаров"):
            assert cards_count > 0

        with allure.step("Проверить бренд каждого товара"):
            for i in range(cards_count):
                product_card = catalog_page.product_cards.nth(i)

                product_brand = product_card.get_attribute(
                    "data-brand"
                )

                logger.info(f"Товар {i}: бренд {product_brand}")

                assert product_brand == "apple"

    @allure.title("Сброс фильтров каталога")
    def test_catalog_reset_filters(self, logged_in_catalog):
        logger.info("Начинаем тест сброса фильтров")

        catalog_page = logged_in_catalog

        with allure.step("Проверить отображение товаров"):
            expect(catalog_page.product_cards.first).to_be_visible()

        with allure.step("Получить исходное количество товаров"):
            initial_count = catalog_page.product_cards.count()

        logger.info(f"Количество товаров до фильтрации: {initial_count}")

        with allure.step("Применить фильтр по бренду Apple"):
            catalog_page.select_brand()

        with allure.step("Проверить активность фильтра"):
            expect(catalog_page.brand_filter).to_have_attribute(
                "data-active", "true"
            )

        with allure.step("Дождаться отображения товаров Apple"):
            catalog_page.page.wait_for_function(
                """() => {
                    const cards = document.querySelectorAll(
                        '[data-testid="product-card"]'
                    );
                    return cards.length > 0 &&
                        Array.from(cards).every(card =>
                            card.getAttribute('data-brand') === 'apple'
                        );
                }"""
            )

        with allure.step("Получить количество товаров Apple"):
            cards_count = catalog_page.product_cards.count()

        logger.info(f"Количество товаров Apple: {cards_count}")

        with allure.step("Проверить наличие товаров"):
            assert cards_count > 0

        with allure.step("Проверить бренд каждого товара"):
            for i in range(cards_count):
                product_card = catalog_page.product_cards.nth(i)

                product_brand = product_card.get_attribute(
                    "data-brand"
                )

                logger.info(f"Товар {i}: бренд {product_brand}")

                assert product_brand == "apple"

        with allure.step("Сбросить фильтры каталога"):
            catalog_page.reset_filters()

        with allure.step("Проверить, что фильтр бренда неактивен"):
            expect(catalog_page.brand_filter).to_have_attribute(
                "data-active", "false"
            )

        with allure.step("Проверить восстановление количества товаров"):
            expect(catalog_page.product_cards).to_have_count(initial_count)

        with allure.step("Получить бренды товаров после сброса"):
            brands = []

            cards_count = catalog_page.product_cards.count()

            for i in range(cards_count):
                product_card = catalog_page.product_cards.nth(i)
                brand = product_card.get_attribute("data-brand")
                brands.append(brand)

        logger.info(f"Бренды после сброса: {brands}")

        with allure.step("Проверить наличие товаров других брендов"):
            assert any(brand != "apple" for brand in brands)


@allure.epic("Интернет-магазин")
@allure.feature("Каталог")
@allure.story("Сортировка товаров")
class TestCatalogSorting:

    @allure.title("Сортировка товаров по возрастанию цены")
    def test_catalog_sorting(self, logged_in_catalog):
        logger.info("Начинаем тест сортировки товаров")

        catalog_page = logged_in_catalog

        with allure.step("Выбрать сортировку по возрастанию цены"):
            catalog_page.sort_by_price_ascending()

        with allure.step("Проверить выбранный вариант сортировки"):
            expect(catalog_page.sort_dropdown).to_have_value(
                "price_asc"
            )

        with allure.step("Дождаться сортировки товаров"):
            catalog_page.page.wait_for_function(
                """() => {
                    const elements = document.querySelectorAll(
                        '[data-testid="product-price"]'
                    );

                    if (elements.length < 2) {
                        return false;
                    }

                    const prices = Array.from(elements).map(element => {
                        const value = element.getAttribute('data-price-cents');

                        return value === null ? NaN : Number(value);
                    });

                    return prices.every(Number.isFinite) &&
                        prices.every((price, index) =>
                            index === 0 || price >= prices[index - 1]
                        );
                }"""
            )

        with allure.step("Получить количество цен товаров"):
            prices_count = catalog_page.product_prices.count()

        with allure.step("Проверить наличие минимум двух товаров"):
            assert prices_count > 1

        with allure.step("Собрать цены всех товаров"):
            prices = []

            for i in range(prices_count):
                price_element = catalog_page.product_prices.nth(i)
                price = int(
                    price_element.get_attribute("data-price-cents")
                )
                prices.append(price)

        logger.info(f"Цены товаров: {prices}")

        with allure.step("Проверить сортировку цен по возрастанию"):
            assert prices == sorted(prices)