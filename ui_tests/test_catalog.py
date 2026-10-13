import logging

from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_catalog_displays_products(logged_in_catalog):
    logger.info("Начинаем тест отображения товаров")

    catalog_page = logged_in_catalog

    logger.info("Проверяем отображение товаров в каталоге")

    expect(catalog_page.product_cards.first).to_be_visible()


def test_catalog_search(logged_in_catalog):
    logger.info("Начинаем тест поиска товаров")

    catalog_page = logged_in_catalog

    catalog_page.search("iPhone")

    logger.info("Проверяем результат поиска")

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

    cards_count = catalog_page.product_cards.count()

    logger.info(f"Количество найденных товаров: {cards_count}")

    assert cards_count > 0


def test_catalog_category_filter(logged_in_catalog):
    logger.info("Начинаем тест фильтрации по категории")

    catalog_page = logged_in_catalog

    catalog_page.select_smartphones()

    expect(catalog_page.smartphones_filter).to_have_attribute(
        "data-active", "true"
    )

    category_id = catalog_page.smartphones_filter.get_attribute(
        "data-category-id"
    )

    assert category_id is not None

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
    cards_count = catalog_page.product_cards.count()

    logger.info(f"Количество смартфонов: {cards_count}")

    assert cards_count > 0

    for i in range(cards_count):
        product_card = catalog_page.product_cards.nth(i)
        product_category = product_card.get_attribute(
            "data-category-id"
        )
        logger.info(
            f"Товар {i}: категория {product_category}"
        )
        assert product_category == category_id


def test_catalog_brand_filter(logged_in_catalog):
    logger.info("Начинаем тест фильтрации по бренду")

    catalog_page = logged_in_catalog

    catalog_page.select_brand()

    expect(catalog_page.brand_filter).to_have_attribute(
        "data-active", "true"
    )
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
    cards_count = catalog_page.product_cards.count()

    logger.info(f"Количество товаров Apple: {cards_count}")

    assert cards_count > 0

    for i in range(cards_count):
        product_card = catalog_page.product_cards.nth(i)

        product_brand = product_card.get_attribute(
            "data-brand"
        )

        logger.info(f"Товар {i}: бренд {product_brand}")

        assert product_brand == "apple"


def test_catalog_sorting(logged_in_catalog):
    logger.info("Начинаем тест сортировки товаров")

    catalog_page = logged_in_catalog

    catalog_page.sort_by_price_ascending()

    expect(catalog_page.sort_dropdown).to_have_value(
        "price_asc"
    )
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
    prices_count = catalog_page.product_prices.count()

    assert prices_count > 1

    prices = []

    for i in range(prices_count):
        price_element = catalog_page.product_prices.nth(i)
        price = int(
            price_element.get_attribute("data-price-cents")
        )
        prices.append(price)

    logger.info(f"Цены товаров: {prices}")

    assert prices == sorted(prices)


def test_catalog_reset_filters(logged_in_catalog):
    logger.info("Начинаем тест сброса фильтров")

    catalog_page = logged_in_catalog

    expect(catalog_page.product_cards.first).to_be_visible()

    initial_count = catalog_page.product_cards.count()

    logger.info(f"Количество товаров до фильтрации: {initial_count}")

    catalog_page.select_brand()

    expect(catalog_page.brand_filter).to_have_attribute(
        "data-active", "true"
    )
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
    cards_count = catalog_page.product_cards.count()

    logger.info(f"Количество товаров Apple: {cards_count}")

    assert cards_count > 0

    for i in range(cards_count):
        product_card = catalog_page.product_cards.nth(i)

        product_brand = product_card.get_attribute(
            "data-brand"
        )

        logger.info(f"Товар {i}: бренд {product_brand}")

        assert product_brand == "apple"

    catalog_page.reset_filters()

    expect(catalog_page.brand_filter).to_have_attribute(
        "data-active", "false"
    )

    expect(catalog_page.product_cards).to_have_count(initial_count)

    brands = []

    cards_count = catalog_page.product_cards.count()

    for i in range(cards_count):
        product_card = catalog_page.product_cards.nth(i)
        brand = product_card.get_attribute("data-brand")
        brands.append(brand)

    logger.info(f"Бренды после сброса: {brands}")

    assert any(brand != "apple" for brand in brands)
