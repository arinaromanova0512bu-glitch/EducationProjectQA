import logging

from playwright.sync_api import Page

from config import UI_BASE_URL
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = UI_BASE_URL

        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Пароль")
        self.name_input = page.get_by_label("Имя")

        self.login_button = page.get_by_role("button", name="Войти")
        self.registration_tab = page.get_by_text("Регистрация", exact=True)
        self.registration_button = page.get_by_role("button", name="Создать аккаунт")
        self.error_message = page.get_by_test_id("auth-error")

    def login(self, email: str, password: str):
        logger.info(f"Попытка входа с email: {email}")
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        logger.info("Нажата кнопка входа")

    def register(self, name: str, email: str, password: str):
        logger.info(f"Попытка регистрации с email: {email}")
        self.click(self.registration_tab)
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.registration_button)
        logger.info("Нажата кнопка регистрации")

    def get_error_message(self):
        logger.info("Получаем сообщение об ошибке авторизации")
        error = self.get_text(self.error_message)
        logger.info(f"Сообщение об ошибке: {error}")
        return error

