import pytest

from faker import Faker
from playwright.sync_api import Page, expect

from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.orders_page import OrdersPage


@pytest.fixture
def auth_page(page: Page):
    return AuthPage(page)


@pytest.fixture
def catalog_page(page: Page):
    return CatalogPage(page)


@pytest.fixture
def new_user():
    fake = Faker()

    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(
            length=12,
            special_chars=False
        )
    }


@pytest.fixture
def logged_in_catalog(auth_page, catalog_page, new_user):
    auth_page.open(auth_page.url)

    auth_page.register(
        new_user["name"],
        new_user["email"],
        new_user["password"]
    )

    auth_page.page.wait_for_url("**/#/catalog")

    return catalog_page


@pytest.fixture
def add_to_cart(empty_cart):
    empty_cart.add_to_cart()
    return empty_cart


@pytest.fixture
def cart_page(page: Page):
    return CartPage(page)


@pytest.fixture
def empty_cart(logged_in_catalog, cart_page):
    cart_page.open_cart()
    cart_page.remove_promo()
    cart_page.clear_cart()
    logged_in_catalog.open_catalog()

    return logged_in_catalog


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def checkout_with_product(add_to_cart, cart_page, checkout_page):
    cart_page.open_cart()
    cart_page.proceed_to_checkout()
    expect(checkout_page.courier_button).to_be_visible()
    return checkout_page


@pytest.fixture
def checkout_with_address(checkout_with_product):
    checkout_page = checkout_with_product

    checkout_page.select_courier_delivery()

    if not checkout_page.address_form.is_visible():
        checkout_page.toggle_address_form()

    checkout_page.fill_delivery_address(
        city="Москва",
        street="Ленина",
        building="10",
        apartment="25",
        recipient="Анна Иванова",
        phone="+79999124567"
    )

    checkout_page.save_delivery_address()

    expect(checkout_page.address_options.first).to_be_visible()

    return checkout_page


@pytest.fixture
def checkout_new_user(
    new_user,
    auth_page,
    catalog_page,
    cart_page,
    checkout_page
):
    auth_page.open(auth_page.url)

    auth_page.register(
        new_user["name"],
        new_user["email"],
        new_user["password"]
    )

    auth_page.page.wait_for_url("**/#/catalog")

    catalog_page.add_to_cart()

    cart_page.open_cart()
    cart_page.proceed_to_checkout()

    expect(checkout_page.courier_button).to_be_visible()

    return checkout_page


@pytest.fixture
def payment_with_product(checkout_with_product):
    checkout_page = checkout_with_product

    checkout_page.select_pickup_delivery()
    checkout_page.select_pickup_point(index=0)

    expect(checkout_page.pay_button).to_be_enabled()

    checkout_page.proceed_to_payment()

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    return checkout_page


@pytest.fixture
def orders_page(page):
    return OrdersPage(page)


@pytest.fixture
def paid_order(payment_with_product, orders_page):
    checkout_page = payment_with_product

    checkout_page.fill_card(
        "4111111111111111",
        "12/28",
        "123",
        "IVAN IVANOV"
    )

    checkout_page.submit_payment_button.click()

    expect(checkout_page.threeds_modal).to_be_visible()

    otp_code = checkout_page.threeds_otp_hint.get_attribute("data-otp")
    assert otp_code, "Не удалось получить SMS-код"

    checkout_page.confirm_3ds(otp_code)

    expect(orders_page.placed_notice).to_be_visible()

    order_id = orders_page.placed_notice.get_attribute("data-order-id")
    assert order_id, "Не удалось получить ID заказа"

    expect(orders_page.order_cards.first).to_be_visible()

    return orders_page