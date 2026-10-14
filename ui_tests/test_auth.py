import logging

import allure
import pytest

logger = logging.getLogger(__name__)


@allure.epic("Интернет-магазин")
@allure.feature("Авторизация")
@allure.story("Вход в систему")
class TestLogin:

    @pytest.mark.smoke
    @allure.title("Страница авторизации открывается")
    def test_open_auth_page(self, auth_page):
        logger.info("Начинаем тест открытия страницы авторизации")

        with allure.step("Открыть страницу авторизации"):
            auth_page.open(auth_page.url)

        with allure.step("Проверить видимость кнопки входа"):
            assert auth_page.is_element_visible(auth_page.login_button)

        logger.info("Страница авторизации успешно открыта")

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "email, password",
        [
            ("admin@store.local", "admin123")
        ]
    )
    @allure.title("Пользователь входит с корректными данными")
    def test_login(self, auth_page, email, password):
        logger.info(f"Начинаем тест логина для пользователя: {email}")

        with allure.step("Открыть страницу авторизации"):
            auth_page.open(auth_page.url)

        with allure.step("Войти с корректными учётными данными"):
            auth_page.login(email, password)

        with allure.step("Проверить переход в каталог после входа"):
            auth_page.page.wait_for_url("**/#/catalog")
            assert "#/catalog" in auth_page.page.url

        logger.info(
            f"Авторизация завершена. Текущий URL: {auth_page.page.url}"
        )

    @pytest.mark.smoke
    @allure.title("Сообщение об ошибке при неверном пароле")
    def test_login_with_invalid_password(self, auth_page):
        logger.info("Начинаем тест логина с неверным паролем")

        with allure.step("Открыть страницу авторизации"):
            auth_page.open(auth_page.url)

        with allure.step("Попробовать войти с неверным паролем"):
            auth_page.login(
                "admin@store.local",
                "wrongpassword"
            )

        with allure.step("Проверить сообщение об ошибке"):
            error = auth_page.get_error_message()
            assert error == "неверный email или пароль"

    @pytest.mark.smoke
    @allure.title("Пустые поля email и пароля не проходят валидацию")
    def test_login_with_empty_fields(self, auth_page):
        logger.info("Начинаем тест логина с пустыми полями")

        with allure.step("Открыть страницу авторизации"):
            auth_page.open(auth_page.url)

        with allure.step("Попробовать войти с пустыми полями"):
            auth_page.login("", "")

        with allure.step("Проверить невалидность email и пароля"):
            assert auth_page.is_element_valid(auth_page.email_input) is False
            assert auth_page.is_element_valid(auth_page.password_input) is False

        logger.info("Поля email и пароля невалидны, если они пустые")


@allure.epic("Интернет-магазин")
@allure.feature("Регистрация")
@allure.story("Регистрация пользователя")
class TestRegistration:

    @pytest.mark.smoke
    @allure.title("Новый пользователь успешно регистрируется")
    def test_successful_registration(self, auth_page, new_user):
        logger.info("Начинаем тест регистрации нового пользователя")

        with allure.step("Открыть страницу регистрации"):
            auth_page.open(auth_page.url)

        with allure.step("Зарегистрировать нового пользователя"):
            auth_page.register(
                new_user["name"],
                new_user["email"],
                new_user["password"]
            )

        with allure.step("Проверить переход в каталог после регистрации"):
            auth_page.page.wait_for_url("**/#/catalog")
            assert "#/catalog" in auth_page.page.url

        logger.info(
            f"Регистрация завершена. Текущий URL: {auth_page.page.url}"
        )

    @pytest.mark.smoke
    @allure.title("Регистрация с существующим email отклоняется")
    def test_registration_with_existing_email(self, auth_page, new_user):
        logger.info("Начинаем тест регистрации нового пользователя")

        with allure.step("Открыть страницу регистрации"):
            auth_page.open(auth_page.url)

        with allure.step(
            "Попробовать зарегистрироваться с существующим email"
        ):
            auth_page.register(
                new_user["name"],
                "admin@store.local",
                new_user["password"]
            )

        with allure.step("Проверить ошибку дублирования email"):
            error = auth_page.get_error_message()

            assert error == (
                'ошибка регистрации: create user: ERROR: duplicate key value '
                'violates unique constraint "users_email_key" (SQLSTATE 23505)'
            )


@allure.epic("Интернет-магазин")
@allure.feature("Авторизация")
@allure.story("Выход из аккаунта")
class TestLogout:

    @pytest.mark.smoke
    @allure.title("Авторизованный пользователь выходит из аккаунта")
    def test_logout(self, auth_page, catalog_page):
        logger.info("Начинаем тест logout")

        with allure.step("Открыть страницу авторизации"):
            auth_page.open(auth_page.url)

        with allure.step("Авторизоваться в магазине"):
            auth_page.login(
                "admin@store.local",
                "admin123"
            )

        with allure.step("Проверить успешный вход в каталог"):
            auth_page.page.wait_for_url("**/#/catalog")
            assert "#/catalog" in auth_page.page.url

        logger.info("Пользователь авторизован, выполняем logout")

        with allure.step("Выйти из аккаунта"):
            catalog_page.logout()

        with allure.step("Проверить переход на страницу входа"):
            catalog_page.page.wait_for_url("**/#/login")
            assert "#/login" in catalog_page.page.url

        logger.info(
            f"Logout завершён. Текущий URL: {catalog_page.page.url}"
        )