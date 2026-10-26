import logging

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_link = page.get_by_test_id("nav-cart")
        self.cart_badge = page.get_by_test_id("cart-badge")
        self.cart_list = page.get_by_test_id("cart-list")
        self.cart_items = page.get_by_test_id("cart-item")
        self.cart_item_names = page.get_by_test_id("cart-item-name")
        self.cart_item_meta = page.get_by_test_id("cart-item-meta")
        self.remove_buttons = page.get_by_test_id("remove-item")
        self.cart_summary = page.get_by_test_id("cart-summary")
        self.cart_item_brands = page.get_by_test_id("cart-item-brand")
        self.cart_item_quantities = page.get_by_test_id("cart-item-qty")
        self.cart_item_line_totals = page.get_by_test_id("cart-item-line-total")
        self.cart_subtotal = page.get_by_test_id("cart-subtotal")
        self.cart_discount = page.get_by_test_id("cart-discount")
        self.cart_total = page.get_by_test_id("cart-total")
        self.cart_expires = page.get_by_test_id("cart-expires")

        self.promo_input = page.get_by_test_id("promo-input")
        self.promo_apply_button = page.get_by_test_id("promo-apply")

        self.checkout_button = page.get_by_test_id("checkout-button")
        self.clear_cart_button = page.get_by_test_id("clear-cart-button")
        self.promo_clear_button = page.get_by_test_id("promo-clear")
        self.cart_empty = page.get_by_test_id("cart-empty")

    def open_cart(self):
        logger.info("Переходим в корзину")

        with self.page.expect_response(
                lambda response: (
                        "/v1/users/" in response.url
                        and response.url.endswith("/cart")
                        and response.request.method == "GET"
                        and response.status == 200
                )
        ):
            self.click(self.cart_link)
        expect(self.cart_discount).to_be_visible()

    def remove_item(self):
        logger.info("Удаляем товар из корзины")
        self.click(self.remove_buttons.first)

    def clear_cart(self):
        if self.cart_items.count() > 0:
            logger.info("Очищаем корзину")
            self.click(self.clear_cart_button)
            expect(self.cart_empty).to_be_visible()
        else:
            logger.info("Корзина уже пуста, очищать нечего")

    def apply_promo(self, promo_code):
        logger.info("Применяем промокод")

        self.fill(self.promo_input, promo_code)
        self.click(self.promo_apply_button)


    def remove_promo(self):
        if self.promo_clear_button.is_visible():
            logger.info("Убираем промокод")
            self.click(self.promo_clear_button)
            expect(self.promo_clear_button).to_be_hidden()
        else:
            logger.info("Корзина уже без промокода, очищать нечего")
        expect(self.cart_discount).to_contain_text("0,00")

    def proceed_to_checkout(self):
        logger.info("Переходим на чекаут")

        self.click(self.checkout_button)

