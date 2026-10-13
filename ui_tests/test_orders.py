import logging
import re

from playwright.sync_api import expect


logger = logging.getLogger(__name__)


def test_orders_page_displayed(logged_in_catalog, orders_page):
    logger.info("Начинаем тест открытия страницы заказов")
    logger.info("Открыть страницу заказов")

    orders_page.open()

    logger.info("Проверить отображение заголовка «Заказы»")
    expect(orders_page.title).to_be_visible()
    expect(orders_page.title).to_have_text("Заказы")

    logger.info("Проверить отображение списка заказов")
    expect(orders_page.orders_page).to_be_visible()


def test_orders_list_displayed(logged_in_catalog, orders_page):
    logger.info("Начинаем тест отображения списка заказов")
    logger.info("Открыть страницу заказов")

    orders_page.open()

    expect(orders_page.orders_page).to_be_visible()
    assert orders_page.order_cards.count() > 0
    expect(orders_page.order_cards.first).to_be_visible()

    logger.info("Проверить наличие идентификатора заказа")
    order_id = orders_page.order_cards.first.get_attribute("data-order-id")

    logger.info("Проверить, что идентификатор заказа не пустой")
    assert order_id is not None and order_id.strip(), "Идентификатор заказа отсутствует"


def test_order_information_displayed(logged_in_catalog, orders_page):
    logger.info("Начинаем тест отображения информации в карточке заказа")
    logger.info("Открыть страницу «Заказы»")
    orders_page.open()

    logger.info("Проверить наличие хотя бы одной карточки заказа")
    expect(orders_page.order_cards.first).to_be_visible()

    logger.info("Выбрать первую карточку заказа")
    order_card = orders_page.order_cards.first

    logger.info("Проверить наличие идентификатора заказа")
    order_id = order_card.get_attribute("data-order-id")
    assert order_id is not None and order_id.strip(), "Идентификатор заказа отсутствует"

    logger.info("Проверить отображение даты и времени оформления заказа")
    order_text = order_card.inner_text()
    assert re.search(r"\d{2}\.\d{2}\.\d{4}", order_text), \
        "Дата оформления заказа отсутствует"
    assert re.search(r"\d{2}:\d{2}", order_text), \
        "Время оформления заказа отсутствует"
    # проверка формата, значение не важно

    logger.info("Проверить наличие хотя бы одного товара")
    order_items = order_card.get_by_test_id("order-item")
    expect(order_items.first).to_be_visible()

    logger.info("Проверить отображение названия товара")
    first_item = order_items.first
    expect(first_item).not_to_be_empty()

    logger.info("Проверить отображение количества товара")
    assert re.search(r"qty\s*\d+", first_item.inner_text()), \
        "Количество товара отсутствует"

    logger.info("Проверить отображение стоимости товара")
    assert re.search(r"\d[\d\s]*,\d{2}", first_item.inner_text()), \
        "Стоимость товара отсутствует"

    logger.info("Проверить отображение способа доставки")
    delivery_method = order_card.get_by_test_id("order-delivery-method")
    expect(delivery_method).to_be_visible()
    expect(delivery_method).not_to_be_empty()

    logger.info("Проверить отображение информации о доставке")
    delivery_info = order_card.get_by_test_id("order-delivery-info")
    expect(delivery_info).to_be_visible()
    expect(delivery_info).not_to_be_empty()


def test_order_status_displayed(logged_in_catalog, orders_page):
    logger.info("Начинаем тест отображения статуса заказа")
    logger.info("Открыть страницу «Заказы»")
    orders_page.open()

    logger.info("Проверить наличие хотя бы одной карточки заказа")
    expect(orders_page.order_cards.first).to_be_visible()

    logger.info("Выбрать первую карточку заказа")
    order_card = orders_page.order_cards.first

    logger.info("Проверить отображение статуса заказа")
    expect(order_card.get_by_test_id("order-status")).to_be_visible()

    logger.info("Получить статус заказа")
    status = order_card.get_attribute("data-status")

    logger.info("Проверить, что статус заказа не пустой")
    assert status is not None and status.strip(), "Статус заказа отсутствует"


def test_order_total_displayed(logged_in_catalog, orders_page):
    logger.info("Начинаем тест отображения итоговой стоимости заказа")
    logger.info("Открыть страницу «Заказы»")
    orders_page.open()

    logger.info("Проверить наличие хотя бы одной карточки заказа")
    expect(orders_page.order_cards.first).to_be_visible()

    logger.info("Выбрать первую карточку заказа")
    order_card = orders_page.order_cards.first

    logger.info("Проверить отображение итоговой стоимости заказа")
    expect(order_card.get_by_test_id("order-total")).to_be_visible()

    logger.info("Получить итоговую стоимость заказа")
    order_total = order_card.get_by_test_id("order-total")
    total_cents = order_total.get_attribute("data-cents")

    logger.info("Проверить, что стоимость заказа не пустая")
    assert total_cents is not None and total_cents.strip(), "Стоимость заказа отсутствует"

    logger.info("Проверить, что итоговая стоимость заказа больше нуля")
    assert int(total_cents) > 0, "Итоговая стоимость заказа должна быть больше нуля"


def test_orders_count_matches_list(logged_in_catalog, orders_page):
    logger.info("Начинаем тест проверки количества заказов")

    logger.info("Открыть страницу «Заказы»")
    orders_page.open()

    logger.info("Проверить отображение счётчика заказов")
    expect(orders_page.subtitle).to_be_visible()

    logger.info("Получить текст счётчика заказов")
    orders_count_text = orders_page.subtitle.inner_text()

    logger.info("Извлечь количество заказов из счётчика")
    displayed_count = int(orders_count_text.split()[0])

    logger.info("Получить фактическое количество карточек заказов")
    actual_count = orders_page.order_cards.count()

    logger.info("Сравнить количество заказов в счётчике с количеством карточек")
    assert displayed_count == actual_count, (
        f"Количество заказов не совпадает: "
        f"в счётчике {displayed_count}, фактически {actual_count}"
    )


def test_empty_orders_list(page, auth_page, orders_page, new_user):
    logger.info("Начинаем тест проверки пустого списка заказов")
    logger.info("Открыть страницу регистрации")

    auth_page.open("http://localhost:8081")

    logger.info("Зарегистрировать нового пользователя")
    auth_page.register(
        name=new_user["name"],
        email=new_user["email"],
        password=new_user["password"]
    )

    logger.info("Дождаться завершения регистрации")
    expect(page).to_have_url("http://localhost:8081/#/catalog")

    logger.info("Открыть страницу «Заказы» через меню")
    page.get_by_role("link", name="Заказы").click()

    logger.info("Проверить переход на страницу заказов")
    expect(page).to_have_url("http://localhost:8081/#/orders")

    logger.info("Проверить отображение заголовка «Заказы»")
    expect(orders_page.title).to_be_visible()
    expect(orders_page.title).to_have_text("Заказы")

    logger.info("Проверить отсутствие карточек заказов")
    expect(orders_page.order_cards).to_have_count(0)

    logger.info("Проверить сообщение о пустой истории заказов")
    expect(orders_page.subtitle).to_have_text("Пока пусто")


def test_paid_order_appears_in_orders(payment_with_product, orders_page):
    checkout_page = payment_with_product
    page = checkout_page.page

    logger.info("Начинаем тест появления оплаченного заказа в истории")

    logger.info("Проверить, что пользователь находится на этапе оплаты")
    expect(
        page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Ввести номер банковской карты")
    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести срок действия карты")
    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести CVC")
    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")
    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Нажать кнопку «Оплатить»")
    checkout_page.submit_payment_button.click()

    logger.info("Проверить появление окна 3D Secure")
    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Получить тестовый SMS-код")
    otp_code = checkout_page.threeds_otp_hint.get_attribute("data-otp")

    assert otp_code, "Не удалось получить SMS-код"

    logger.info("Ввести SMS-код")
    checkout_page.threeds_otp.fill(otp_code)

    logger.info("Подтвердить оплату")
    expect(checkout_page.threeds_confirm_button).to_be_enabled()
    checkout_page.threeds_confirm_button.click()

    logger.info("Проверить успешное завершение оплаты")
    expect(checkout_page.threeds_modal).not_to_be_visible()
    expect(checkout_page.card_form).not_to_be_visible()

    logger.info("Дождаться появления уведомления о новом заказе")
    expect(orders_page.placed_notice).to_be_visible()

    logger.info("Получить ID нового заказа")
    order_id = orders_page.placed_notice.get_attribute("data-order-id")

    assert order_id, "Не удалось получить ID созданного заказа"

    logger.info("Проверить, что открыта история заказов")
    expect(page).to_have_url(re.compile(r".*/#/orders\?placed=[\w-]+"))
    expect(orders_page.title).to_be_visible()

    logger.info("Найти созданный заказ по ID")

    order_card = page.locator(
        f'[data-testid="order-card"][data-order-id="{order_id}"]'
    )

    expect(order_card).to_have_count(1)

    logger.info("Проверить статус нового заказа")
    expect(
        order_card.get_by_test_id("order-status")
    ).to_have_text("Оплачен")

    expect(order_card).to_have_attribute("data-status", "PAID")

    logger.info("Проверить наличие товара в заказе")
    expect(
        order_card.get_by_test_id("order-item").first
    ).to_be_visible()

    logger.info("Проверить итоговую стоимость заказа")
    order_total = order_card.get_by_test_id("order-total")

    expect(order_total).to_be_visible()

    total_cents = order_total.get_attribute("data-cents")

    assert total_cents is not None, "Стоимость заказа отсутствует"
    assert int(total_cents) > 0, "Стоимость заказа должна быть больше нуля"