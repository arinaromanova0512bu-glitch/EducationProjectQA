import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CatalogPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.logout_button = page.get_by_role("button", name="Выйти")
        self.product_cards = page.get_by_test_id("product-card")
        self.search_input = page.get_by_test_id("catalog-search")
        self.smartphones_filter = page.get_by_test_id("filter-category-phones")
        self.brand_filter = page.get_by_test_id("filter-apple-label").locator("..")

        self.sort_dropdown = page.get_by_test_id("catalog-sort")
        self.product_prices = page.get_by_test_id("product-price")
        self.reset_filters_button = page.get_by_test_id("filters-reset")
        self.catalog_link = page.get_by_test_id("nav-catalog")

        self.add_to_cart_buttons = page.get_by_test_id("add-to-cart")

    def logout(self):
        logger.info("Попытка выхода из аккаунта")

        self.click(self.logout_button)
        logger.info("Нажата кнопка выхода")

    def search(self, query: str):
        logger.info("Выполняем поиск товаров")

        self.fill(self.search_input, query)

    def select_smartphones(self):
        logger.info("Выбираем категорию смартфонов")

        self.click(self.smartphones_filter)

    def select_brand(self):
        logger.info("Выбираем бренд")

        self.click(self.brand_filter)

    def sort_by_price_ascending(self):
        logger.info("Сортируем товары по возрастанию цены")

        self.sort_dropdown.select_option("price_asc")

    def reset_filters(self):
        logger.info("Сбрасываем фильтры каталога")

        self.click(self.reset_filters_button)

    def open_catalog(self):
        logger.info("Возвращаемся в каталог")

        self.click(self.catalog_link)

    def add_to_cart(self, index=0):
        logger.info(f"Добавляем товар с индексом {index} в корзину")

        self.click(self.add_to_cart_buttons.nth(index))