import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.courier_button = page.get_by_test_id("delivery-method-courier")
        self.pickup_button = page.get_by_test_id("delivery-method-pickup")
        self.pay_button = page.get_by_test_id("checkout-to-payment")
        self.pickup_options = page.get_by_test_id("pickup-option")
        self.address_toggle_button = page.get_by_test_id("address-add-toggle") # скрыть форму
        self.address_form = page.get_by_test_id("address-form")
        self.city_input = page.get_by_test_id("address-city")
        self.street_input = page.get_by_test_id("address-street")
        self.building_input = page.get_by_test_id("address-building")
        self.apartment_input = page.get_by_test_id("address-apartment")
        self.recipient_input = page.get_by_test_id("address-recipient")
        self.phone_input = page.get_by_test_id("address-phone")

        self.save_address_button = page.get_by_test_id("address-save")
        self.subtotal = page.get_by_test_id("checkout-subtotal")
        self.delivery_fee = page.get_by_test_id("checkout-delivery-fee")
        self.total = page.get_by_test_id("checkout-total")
        self.address_options = page.get_by_test_id("address-option")
        self.toast = page.get_by_test_id("toast") # ошибка при пустых полях
        self.checkout_back = page.get_by_test_id("checkout-back-delivery")

        self.card_form = page.get_by_test_id("card-form")
        self.card_visual = page.get_by_test_id("card-visual")
        self.card_pan = page.get_by_test_id("card-pan")
        self.card_expiry = page.get_by_test_id("card-expiry")
        self.card_cvc = page.get_by_test_id("card-cvc")
        self.card_holder = page.get_by_test_id("card-holder")
        self.submit_payment_button = page.get_by_test_id("pay-button")

        self.threeds_modal = page.get_by_test_id("threeds-modal")
        self.threeds_otp = page.get_by_test_id("threeds-otp")
        self.threeds_otp_hint = page.get_by_test_id("threeds-otp-hint")
        self.threeds_confirm_button = page.get_by_test_id("threeds-confirm")
        self.threeds_cancel_button = page.get_by_test_id("threeds-cancel")

    def select_pickup_point(self, index=0):
        logger.info("Выбор пункта выдачи")

        self.click(self.pickup_options.nth(index))

    def select_courier_delivery(self):
        logger.info("Выбор курьерской доставки")

        self.click(self.courier_button)

    def select_pickup_delivery(self):
        logger.info("Выбор самовывоза")

        self.click(self.pickup_button)

    def fill_delivery_address(
            self, city, street, building,
            apartment, recipient, phone
    ):
        logger.info("Заполнение адреса курьерской доставки")

        self.fill(self.city_input, city)
        self.fill(self.street_input, street)
        self.fill(self.building_input, building)
        self.fill(self.apartment_input, apartment)
        self.fill(self.recipient_input, recipient)
        self.fill(self.phone_input, phone)

    def save_delivery_address(self):
        logger.info("Сохранение адреса доставки")

        self.click(self.save_address_button)

    def toggle_address_form(self):
        logger.info("Переключение видимости формы")

        self.click(self.address_toggle_button)

    def proceed_to_payment(self):
        logger.info("Переход к оплате")

        self.click(self.pay_button)

    def return_to_delivery(self):
        logger.info("Возврат к выбору доставки")

        self.click(self.checkout_back)