import logging

from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_select_courier_delivery(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест выбора курьерской доставки")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    logger.info("Проверить, что курьерская доставка выбрана")
    expect(checkout_page.courier_button).to_have_attribute(
        "data-active", "true"
    )

    logger.info("Проверить отображение сохранённых адресов")
    expect(checkout_page.address_options.first).to_be_visible()


def test_select_pickup_delivery(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест выбора самовывоза")
    logger.info("Выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(
        checkout_page.pickup_button
    ).to_have_attribute("data-active", "true")
    expect(
        checkout_page.courier_button
    ).to_have_attribute("data-active", "false")
    expect(checkout_page.pickup_options.first).to_be_visible()
    expect(checkout_page.delivery_fee).to_have_attribute("data-cents", "0")


def test_select_pickup_point(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест выбора опций самовывоза")
    logger.info("Выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.pickup_options.first).to_be_visible()
    expect(checkout_page.pickup_options).to_have_count(5)

    logger.info("Выбор пункта выдачи")

    checkout_page.select_pickup_point(index=1)

    expect(
        checkout_page.pickup_options.nth(1)
    ).to_have_attribute("data-active", "true")
    expect(
        checkout_page.pickup_options.nth(0)
    ).to_have_attribute("data-active", "false")


def test_switch_delivery_methods(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест выбора опций получения заказа")
    logger.info("Выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.pickup_options.first).to_be_visible()
    expect(checkout_page.pickup_button).to_have_attribute("data-active", "true")

    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    expect(checkout_page.courier_button).to_have_attribute("data-active", "true")
    expect(checkout_page.address_options.first).to_be_visible()
    expect(checkout_page.pickup_button).to_have_attribute("data-active", "false")

    logger.info("Снова выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.pickup_button).to_have_attribute("data-active", "true")
    expect(checkout_page.courier_button).to_have_attribute("data-active", "false")
    expect(checkout_page.pickup_options.first).to_be_visible()


def test_toggle_delivery_address_form(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест открытия и закрытия формы адреса доставки")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    if not checkout_page.address_form.is_visible():
        checkout_page.toggle_address_form()

    expect(checkout_page.address_form).to_be_visible()

    logger.info("Нажать кнопку сворачивания формы адреса")

    checkout_page.toggle_address_form()

    expect(checkout_page.address_form).to_be_hidden()

    logger.info("Повторно открыть форму адреса")

    checkout_page.toggle_address_form()

    expect(checkout_page.address_form).to_be_visible()


def test_save_delivery_address(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест успешного сохранения адреса доставки")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    if not checkout_page.address_form.is_visible():
        checkout_page.toggle_address_form()

    expect(checkout_page.address_form).to_be_visible()

    logger.info("Заполнить поля формы")

    checkout_page.fill_delivery_address(
        city="Москва",
        street="Ленина",
        building="10",
        apartment="25",
        recipient="Анна Иванова",
        phone="+79999124567"
    )

    addresses_before = checkout_page.address_options.count()

    logger.info("Нажать кнопку «Сохранить адрес»")

    checkout_page.save_delivery_address()

    expect(checkout_page.address_options).to_have_count(addresses_before + 1)
    expect(checkout_page.address_options.last).to_be_visible()
    expect(checkout_page.address_options.last).to_contain_text("Москва, Ленина, 10")
    expect(checkout_page.address_options.last).to_have_attribute("data-active", "true")


def test_save_delivery_address_with_whitespace_fields(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Проверка сохранения адреса с пробелами в обязательных полях")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    if not checkout_page.address_form.is_visible():
        checkout_page.toggle_address_form()

    expect(checkout_page.address_form).to_be_visible()

    logger.info("Заполнить обязательные поля только пробелами")

    checkout_page.fill_delivery_address(
        city="   ",
        street="   ",
        building="   ",
        apartment="   ",
        recipient="   ",
        phone="   "
    )

    logger.info("Нажать кнопку «Сохранить адрес»")

    addresses_before = checkout_page.address_options.count()

    expect(checkout_page.save_address_button).to_be_enabled()

    checkout_page.save_delivery_address()

    expect(checkout_page.toast).to_be_visible()
    expect(checkout_page.toast).to_have_attribute("data-toast-type", "error")
    expect(checkout_page.toast).to_have_text("city обязателен")

    expect(checkout_page.address_options).to_have_count(addresses_before)
    expect(checkout_page.address_form).to_be_visible()


def test_cannot_proceed_to_payment_without_delivery_address(checkout_new_user):
    checkout_page = checkout_new_user

    logger.info("Проверка невозможности перехода к оплате без адреса доставки")

    checkout_page.select_courier_delivery()

    logger.info("Проверяем отсутствие сохранённых адресов")
    expect(checkout_page.address_options).to_have_count(0)

    logger.info("Проверяем, что кнопка «К оплате» неактивна")
    expect(checkout_page.pay_button).to_be_disabled()


def test_delivery_fee_changes_when_switching_methods(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Проверка пересчёта стоимости доставки при переключении способов получения")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    expect(checkout_page.delivery_fee).to_have_attribute("data-cents", "29900")

    logger.info("Переключиться на самовывоз")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.delivery_fee).to_have_attribute("data-cents", "0")

    logger.info("Повторно выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    expect(checkout_page.delivery_fee).to_have_attribute("data-cents", "29900")


def test_checkout_total_with_courier_delivery(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Проверка расчёта итоговой стоимости заказа при курьерской доставке")

    checkout_page.select_courier_delivery()

    logger.info("Получить стоимость товаров")

    subtotal = checkout_page.subtotal.inner_text()
    subtotal = int(float(
        subtotal.replace("\xa0", "")
        .replace(" ", "")
        .replace("$", "")
        .replace(",", ".")
    ) * 100)

    logger.info("Получить стоимость доставки")

    delivery_fee = int(checkout_page.delivery_fee.get_attribute("data-cents"))

    logger.info("Получить итоговую стоимость")

    total = checkout_page.total.inner_text()
    total = int(float(
        total.replace("\xa0", "")
        .replace(" ", "")
        .replace("$", "")
        .replace(",", ".")
    ) * 100)
    logger.info("Проверить информацию о скидках на странице")

    logger.info(
        checkout_page.page.locator("body").inner_text()
    )
    logger.info("Вычислить ожидаемую итоговую стоимость")

    expected_total = subtotal + delivery_fee

    logger.info("Сравнить ожидаемую и фактическую стоимость")

    assert total == expected_total, (
        f"Неверная итоговая стоимость: "
        f"ожидалось {expected_total}, получено {total}"
    )


def test_checkout_total_with_pickup_delivery(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Проверка расчёта итоговой стоимости заказа при самовывозе")

    checkout_page.select_pickup_delivery()

    logger.info("Получить стоимость товаров")

    subtotal = checkout_page.subtotal.inner_text()
    subtotal = int(float(
        subtotal.replace("\xa0", "")
        .replace(" ", "")
        .replace("$", "")
        .replace(",", ".")
    ) * 100)

    logger.info("Получить стоимость доставки")

    delivery_fee = int(checkout_page.delivery_fee.get_attribute("data-cents"))

    logger.info("Получить итоговую стоимость")

    total = checkout_page.total.inner_text()
    total = int(float(
        total.replace("\xa0", "")
        .replace(" ", "")
        .replace("$", "")
        .replace(",", ".")
    ) * 100)

    logger.info("Проверить, что самовывоз бесплатный")

    assert delivery_fee == 0, (
        f"Ожидалась бесплатная доставка, получено {delivery_fee}"
    )

    logger.info("Проверить правильность итоговой стоимости")

    expected_total = subtotal + delivery_fee

    assert total == expected_total, (
        f"Неверная итоговая стоимость: "
        f"ожидалось {expected_total}, получено {total}"
    )


def test_proceed_to_payment_with_pickup(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест выбора опций самовывоза")
    logger.info("Выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.pickup_options.first).to_be_visible()

    logger.info("Выбор пункта выдачи")

    checkout_page.select_pickup_point(index=0)

    expect(checkout_page.pickup_options.nth(0)).to_have_attribute("data-active", "true")

    logger.info("Перейти на страницу оплаты")

    expect(checkout_page.pay_button).to_be_enabled()

    checkout_page.proceed_to_payment()

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()


def test_proceed_to_payment_with_courier(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест перехода к оплате при курьерской доставке")
    logger.info("Выбрать способ доставки «Курьер»")

    checkout_page.select_courier_delivery()

    expect(checkout_page.courier_button).to_have_attribute("data-active", "true")

    logger.info("Выбрать первый сохранённый адрес доставки")

    expect(checkout_page.address_options.first).to_be_visible()

    checkout_page.address_options.first.click()

    expect(checkout_page.address_options.first).to_have_attribute("data-active", "true")

    logger.info("Перейти на страницу оплаты")

    expect(checkout_page.pay_button).to_be_enabled()

    checkout_page.proceed_to_payment()

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()


def test_return_to_delivery_from_payment(checkout_with_product):
    checkout_page = checkout_with_product

    logger.info("Начинаем тест возврата с этапа оплаты к выбору доставки")
    logger.info("Выбрать способ доставки «Самовывоз»")

    checkout_page.select_pickup_delivery()

    expect(checkout_page.pickup_options.first).to_be_visible()

    logger.info("Выбор пункта выдачи")

    checkout_page.select_pickup_point(index=0)

    expect(checkout_page.pickup_options.nth(0)).to_have_attribute("data-active", "true")

    logger.info("Перейти на страницу оплаты")

    expect(checkout_page.pay_button).to_be_enabled()

    checkout_page.proceed_to_payment()

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Нажать кнопку возврата к выбору доставки")

    checkout_page.return_to_delivery()

    expect(
        checkout_page.page.get_by_role("heading", name="Доставка")
    ).to_be_visible()
    expect(checkout_page.pickup_button).to_have_attribute("data-active", "true")
    expect(checkout_page.pickup_options.nth(0)).to_have_attribute("data-active", "true")


def test_payment_form_displayed(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест отображения формы оплаты банковской картой")
    logger.info("Проверить отображение заголовка «Оплата»")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Проверить отображение формы оплаты")

    expect(checkout_page.card_form).to_be_visible()
    expect(checkout_page.card_pan).to_be_visible()
    expect(checkout_page.card_expiry).to_be_visible()
    expect(checkout_page.card_cvc).to_be_visible()
    expect(checkout_page.card_holder).to_be_visible()
    expect(checkout_page.submit_payment_button).to_be_visible()
    expect(checkout_page.card_visual).to_be_visible()


def test_fill_payment_form_with_valid_card(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест ввода корректных данных банковской карты")

    logger.info("Ввести номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Проверить введённые данные банковской карты")

    expect(checkout_page.card_pan).to_have_value("4111 1111 1111 1111")
    expect(checkout_page.card_expiry).to_have_value("12/28")
    expect(checkout_page.card_cvc).to_have_value("123")
    expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

    logger.info("Проверить, что форма оплаты отображается")

    expect(checkout_page.card_form).to_be_visible()

    logger.info("Проверить, что кнопка оплаты отображается")

    expect(checkout_page.submit_payment_button).to_be_visible()


def test_payment_with_empty_card_fields(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест оплаты с пустыми полями банковской карты")

    logger.info("Проверить, что форма оплаты отображается")

    expect(checkout_page.card_form).to_be_visible()

    logger.info("Очистить все поля банковской карты")

    checkout_page.card_pan.fill("")
    checkout_page.card_expiry.fill("")
    checkout_page.card_cvc.fill("")
    checkout_page.card_holder.fill("")

    logger.info("Проверить, что все поля банковской карты пустые")

    expect(checkout_page.card_pan).to_be_empty()
    expect(checkout_page.card_expiry).to_be_empty()
    expect(checkout_page.card_cvc).to_be_empty()
    expect(checkout_page.card_holder).to_be_empty()

    logger.info("Проверить, что кнопка оплаты отображается")

    expect(checkout_page.submit_payment_button).to_be_visible()

    logger.info("Нажать кнопку «Оплатить» с пустыми полями")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Проверить, что форма оплаты осталась доступна")

    expect(checkout_page.card_form).to_be_visible()


def test_payment_with_invalid_card_number(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест оплаты с некорректным номером банковской карты")

    logger.info("Ввести некорректный номер банковской карты")

    checkout_page.card_pan.fill("1234567890123456")

    logger.info("Заполнить остальные поля корректными данными")

    checkout_page.card_expiry.fill("12/28")
    checkout_page.card_cvc.fill("123")
    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Проверить, что данные введены")

    expect(checkout_page.card_pan).to_have_value("1234 5678 9012 3456")
    expect(checkout_page.card_expiry).to_have_value("12/28")
    expect(checkout_page.card_cvc).to_have_value("123")
    expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

    logger.info("Попытаться оплатить заказ с некорректным номером карты")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()
    expect(checkout_page.card_form).to_be_visible()


def test_payment_with_expired_card(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест оплаты с истёкшим сроком действия карты")

    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести истёкший срок действия карты")

    checkout_page.card_expiry.fill("12/24")

    logger.info("Ввести корректный CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Проверить введённые данные банковской карты")

    expect(checkout_page.card_pan).to_have_value("4111 1111 1111 1111")
    expect(checkout_page.card_expiry).to_have_value("12/24")
    expect(checkout_page.card_cvc).to_have_value("123")
    expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

    logger.info("Попытаться оплатить заказ с просроченной картой")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()
    expect(checkout_page.card_form).to_be_visible()


def test_payment_with_invalid_cvc(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест оплаты с некорректным CVC")
    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести корректный срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести некорректный CVC")

    checkout_page.card_cvc.fill("12")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Проверить введённые данные банковской карты")

    expect(checkout_page.card_pan).to_have_value("4111 1111 1111 1111")
    expect(checkout_page.card_expiry).to_have_value("12/28")
    expect(checkout_page.card_cvc).to_have_value("12")
    expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

    logger.info("Попытаться оплатить заказ с некорректным CVC")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()
    expect(checkout_page.card_form).to_be_visible()


def test_order_total_on_payment_step(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест проверки итоговой стоимости заказа на этапе оплаты")

    logger.info("Проверить, что пользователь находится на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Проверить отображение стоимости товаров")

    expect(checkout_page.subtotal).to_be_visible()

    logger.info("Проверить отображение стоимости доставки")

    expect(checkout_page.delivery_fee).to_be_visible()

    logger.info("Проверить отображение итоговой стоимости заказа")

    expect(checkout_page.total).to_be_visible()

    logger.info("Получить стоимость товаров, доставки и итоговую сумму")

    subtotal = checkout_page.subtotal.inner_text()
    delivery_fee = checkout_page.delivery_fee.inner_text()
    total = checkout_page.total.inner_text()

    logger.info(f"Стоимость товаров: {subtotal}")
    logger.info(f"Стоимость доставки: {delivery_fee}")
    logger.info(f"Итоговая стоимость: {total}")

    logger.info("Проверить, что стоимость доставки при самовывозе равна нулю")

    assert checkout_page.delivery_fee.get_attribute("data-cents") == "0"
    assert total == subtotal


def test_successful_payment_with_valid_card(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест успешной оплаты заказа банковской картой")
    logger.info("Проверить, что пользователь находится на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести корректный срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести корректный CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Нажать кнопку «Оплатить»")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить появление окна 3D Secure")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Получить тестовый SMS-код")

    otp_code = checkout_page.threeds_otp_hint.get_attribute("data-otp")

    assert otp_code is not None, "Не удалось получить SMS-код"

    logger.info("Ввести SMS-код подтверждения")

    checkout_page.threeds_otp.fill(otp_code)

    logger.info("Проверить, что кнопка подтверждения активна")

    expect(checkout_page.threeds_confirm_button).to_be_enabled()

    logger.info("Подтвердить оплату")

    checkout_page.threeds_confirm_button.click()

    logger.info("Проверить закрытие окна 3D Secure")

    expect(checkout_page.threeds_modal).not_to_be_visible()
    expect(checkout_page.card_form).not_to_be_visible()


def test_payment_with_invalid_3ds_code(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест оплаты с некорректным кодом 3D Secure")
    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести корректный срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести корректный CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Нажать кнопку «Оплатить»")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить появление окна 3D Secure")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Получить корректный SMS-код")

    correct_otp = checkout_page.threeds_otp_hint.get_attribute("data-otp")

    assert correct_otp is not None, "Не удалось получить SMS-код"

    logger.info("Сформировать некорректный SMS-код")

    invalid_otp = "000000" if correct_otp != "000000" else "111111"

    logger.info("Ввести некорректный SMS-код")

    checkout_page.threeds_otp.fill(invalid_otp)

    logger.info("Проверить, что кнопка подтверждения активна")

    expect(checkout_page.threeds_confirm_button).to_be_enabled()

    logger.info("Подтвердить оплату с некорректным SMS-кодом")

    checkout_page.threeds_confirm_button.click()

    logger.info("Проверить, что окно 3D Secure осталось открытым")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(checkout_page.card_form).to_be_visible()


def test_payment_with_empty_3ds_code(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест подтверждения оплаты с пустым SMS-кодом")
    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести корректный срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести корректный CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Нажать кнопку «Оплатить»")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить появление окна 3D Secure")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Проверить, что поле SMS-кода пустое")

    expect(checkout_page.threeds_otp).to_be_empty()

    logger.info("Проверить, что кнопка подтверждения неактивна")

    expect(checkout_page.threeds_confirm_button).to_be_disabled()

    logger.info("Проверить, что окно 3D Secure осталось открытым")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Проверить, что форма оплаты остаётся доступной")

    expect(checkout_page.card_form).to_be_visible()


def test_cancel_3ds_payment(payment_with_product):
    checkout_page = payment_with_product

    logger.info("Начинаем тест отмены оплаты через 3D Secure")

    logger.info("Ввести корректный номер банковской карты")

    checkout_page.card_pan.fill("4111111111111111")

    logger.info("Ввести корректный срок действия карты")

    checkout_page.card_expiry.fill("12/28")

    logger.info("Ввести корректный CVC")

    checkout_page.card_cvc.fill("123")

    logger.info("Ввести имя владельца карты")

    checkout_page.card_holder.fill("IVAN IVANOV")

    logger.info("Нажать кнопку «Оплатить»")

    checkout_page.submit_payment_button.click()

    logger.info("Проверить появление окна 3D Secure")

    expect(checkout_page.threeds_modal).to_be_visible()

    logger.info("Проверить отображение кнопки «Отмена»")

    expect(checkout_page.threeds_cancel_button).to_be_visible()

    logger.info("Нажать кнопку «Отмена»")

    checkout_page.threeds_cancel_button.click()

    logger.info("Проверить закрытие окна 3D Secure")

    expect(checkout_page.threeds_modal).not_to_be_visible()

    logger.info("Проверить, что пользователь остался на этапе оплаты")

    expect(
        checkout_page.page.get_by_role("heading", name="Оплата")
    ).to_be_visible()

    logger.info("Проверить, что форма оплаты осталась доступна")

    expect(checkout_page.card_form).to_be_visible()

    logger.info("Проверить, что кнопка оплаты снова активна")

    expect(checkout_page.submit_payment_button).to_be_enabled()