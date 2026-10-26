import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        logger.info(f"Открываем страницу: {url}")
        self.page.goto(url)

    def click(self, element):
        logger.info("Нажимаем на элемент")
        element.click()

    def fill(self, element, value):
        logger.info("Заполняем поле")
        element.fill(value)

    def get_text(self, element):
        logger.info("Получаем текст элемента")
        return element.text_content()

    def is_element_visible(self, element):
        logger.info("Проверяем видимость элемента")
        return element.is_visible()

    def wait_for_element(self, element):
        logger.info("Ожидаем появления элемента")
        element.wait_for()

    def is_element_valid(self, element):
        logger.info("Проверяем валидность элемента")
        return element.evaluate("element => element.checkValidity()")