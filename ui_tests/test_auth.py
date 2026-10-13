import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_open_auth_page(auth_page):
    logger.info("Начинаем тест открытия страницы авторизации")

    auth_page.open(auth_page.url)

    assert auth_page.is_element_visible(auth_page.login_button)

    logger.info("Страница авторизации успешно открыта")

@pytest.mark.smoke
@pytest.mark.parametrize(
    "email, password",
    [
        ("admin@store.local",
         "admin123")
    ]
)


def test_login(auth_page, email, password):
    logger.info(f"Начинаем тест логина для пользователя: {email}")

    auth_page.open(auth_page.url)
    auth_page.login(
        email,
        password
    )

    auth_page.page.wait_for_url("**/#/catalog")

    assert "#/catalog" in auth_page.page.url

    logger.info(f"Авторизация завершена. Текущий URL: {auth_page.page.url}")


@pytest.mark.smoke
def test_login_with_invalid_password(auth_page):
    logger.info("Начинаем тест логина с неверным паролем")

    auth_page.open(auth_page.url)
    auth_page.login(
        "admin@store.local",
        "wrongpassword"
    )
    error = auth_page.get_error_message()
    assert error == "неверный email или пароль"


@pytest.mark.smoke
def test_successful_registration(auth_page, new_user):
    logger.info("Начинаем тест регистрации нового пользователя")

    auth_page.open(auth_page.url)
    auth_page.register(
        new_user["name"],
        new_user["email"],
        new_user["password"]
    )

    auth_page.page.wait_for_url("**/#/catalog")

    assert "#/catalog" in auth_page.page.url

    logger.info(f"Регистрация завершена. Текущий URL: {auth_page.page.url}")


@pytest.mark.smoke
def test_registration_with_existing_email(auth_page, new_user):
    logger.info("Начинаем тест регистрации нового пользователя")

    auth_page.open(auth_page.url)
    auth_page.register(
        new_user["name"],
        "admin@store.local",
        new_user["password"]
    )


    error = auth_page.get_error_message()

    assert error == (
        'ошибка регистрации: create user: ERROR: duplicate key value '
        'violates unique constraint "users_email_key" (SQLSTATE 23505)'
    )


@pytest.mark.smoke
def test_login_with_empty_fields(auth_page):
    logger.info("Начинаем тест логина с пустыми полями")

    auth_page.open(auth_page.url)
    auth_page.login("", "")

    assert auth_page.is_element_valid(auth_page.email_input) is False
    assert auth_page.is_element_valid(auth_page.password_input) is False

    logger.info("Поля email и пароля невалидны, если они пустые")


@pytest.mark.smoke
def test_logout(auth_page, catalog_page):
    logger.info("Начинаем тест logout")

    auth_page.open(auth_page.url)
    auth_page.login(
        "admin@store.local",
        "admin123"
    )

    auth_page.page.wait_for_url("**/#/catalog")
    assert "#/catalog" in auth_page.page.url

    logger.info("Пользователь авторизован, выполняем logout")

    catalog_page.logout()

    catalog_page.page.wait_for_url("**/#/login")
    assert "#/login" in catalog_page.page.url

    logger.info(f"Logout завершён. Текущий URL: {catalog_page.page.url}")
