import logging

import allure
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


@allure.epic("Интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Выбор способа доставки")
class TestDeliveryMethods:

    @allure.title("Выбор курьерской доставки")
    def test_select_courier_delivery(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест выбора курьерской доставки")
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        logger.info("Проверить, что курьерская доставка выбрана")

        with allure.step("Проверить активность курьерской доставки"):
            expect(checkout_page.courier_button).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Проверить отображение сохранённых адресов")

        with allure.step("Проверить отображение сохранённых адресов"):
            expect(checkout_page.address_options.first).to_be_visible()

    @allure.title("Выбор самовывоза")
    def test_select_pickup_delivery(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест выбора самовывоза")
        logger.info("Выбрать способ доставки «Самовывоз»")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить активность самовывоза"):
            expect(
                checkout_page.pickup_button
            ).to_have_attribute("data-active", "true")

        with allure.step("Проверить неактивность курьерской доставки"):
            expect(
                checkout_page.courier_button
            ).to_have_attribute("data-active", "false")

        with allure.step("Проверить отображение пунктов самовывоза"):
            expect(checkout_page.pickup_options.first).to_be_visible()

        with allure.step("Проверить бесплатную доставку"):
            expect(checkout_page.delivery_fee).to_have_attribute(
                "data-cents", "0"
            )

    @allure.title("Выбор пункта самовывоза")
    def test_select_pickup_point(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест выбора опций самовывоза")
        logger.info("Выбрать способ доставки «Самовывоз»")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить отображение пяти пунктов выдачи"):
            expect(checkout_page.pickup_options.first).to_be_visible()
            expect(checkout_page.pickup_options).to_have_count(5)

        logger.info("Выбор пункта выдачи")

        with allure.step("Выбрать второй пункт выдачи"):
            checkout_page.select_pickup_point(index=1)

        with allure.step("Проверить активность выбранного пункта"):
            expect(
                checkout_page.pickup_options.nth(1)
            ).to_have_attribute("data-active", "true")

        with allure.step("Проверить неактивность первого пункта"):
            expect(
                checkout_page.pickup_options.nth(0)
            ).to_have_attribute("data-active", "false")

    @allure.title("Переключение способов доставки")
    def test_switch_delivery_methods(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест выбора опций получения заказа")
        logger.info("Выбрать способ доставки «Самовывоз»")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить выбранный способ доставки"):
            expect(checkout_page.pickup_options.first).to_be_visible()
            expect(checkout_page.pickup_button).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Переключиться на курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Проверить переключение на курьера"):
            expect(checkout_page.courier_button).to_have_attribute(
                "data-active", "true"
            )
            expect(checkout_page.address_options.first).to_be_visible()
            expect(checkout_page.pickup_button).to_have_attribute(
                "data-active", "false"
            )

        logger.info("Снова выбрать способ доставки «Самовывоз»")

        with allure.step("Повторно выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить повторное переключение"):
            expect(checkout_page.pickup_button).to_have_attribute(
                "data-active", "true"
            )
            expect(checkout_page.courier_button).to_have_attribute(
                "data-active", "false"
            )
            expect(checkout_page.pickup_options.first).to_be_visible()

@allure.epic("Интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Управление адресами доставки")
class TestDeliveryAddress:

    @allure.title("Открытие и закрытие формы адреса доставки")
    def test_toggle_delivery_address_form(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест открытия и закрытия формы адреса доставки")
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Открыть форму адреса, если она закрыта"):
            if not checkout_page.address_form.is_visible():
                checkout_page.toggle_address_form()

        with allure.step("Проверить отображение формы адреса"):
            expect(checkout_page.address_form).to_be_visible()

        logger.info("Нажать кнопку сворачивания формы адреса")

        with allure.step("Закрыть форму адреса доставки"):
            checkout_page.toggle_address_form()

        with allure.step("Проверить, что форма скрыта"):
            expect(checkout_page.address_form).to_be_hidden()

        logger.info("Повторно открыть форму адреса")

        with allure.step("Повторно открыть форму адреса"):
            checkout_page.toggle_address_form()

        with allure.step("Проверить повторное отображение формы"):
            expect(checkout_page.address_form).to_be_visible()

    @allure.title("Успешное сохранение адреса доставки")
    def test_save_delivery_address(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест успешного сохранения адреса доставки")
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Открыть форму адреса, если она закрыта"):
            if not checkout_page.address_form.is_visible():
                checkout_page.toggle_address_form()

        with allure.step("Проверить отображение формы адреса"):
            expect(checkout_page.address_form).to_be_visible()

        logger.info("Заполнить поля формы")

        with allure.step("Заполнить данные адреса доставки"):
            checkout_page.fill_delivery_address(
                city="Москва",
                street="Ленина",
                building="10",
                apartment="25",
                recipient="Анна Иванова",
                phone="+79999124567"
            )

        with allure.step("Получить количество сохранённых адресов"):
            addresses_before = checkout_page.address_options.count()

        logger.info("Нажать кнопку «Сохранить адрес»")

        with allure.step("Сохранить новый адрес"):
            checkout_page.save_delivery_address()

        with allure.step("Проверить увеличение количества адресов"):
            expect(checkout_page.address_options).to_have_count(
                addresses_before + 1
            )

        with allure.step("Проверить отображение нового адреса"):
            expect(checkout_page.address_options.last).to_be_visible()
            expect(checkout_page.address_options.last).to_contain_text(
                "Москва, Ленина, 10"
            )

        with allure.step("Проверить, что новый адрес выбран"):
            expect(checkout_page.address_options.last).to_have_attribute(
                "data-active", "true"
            )

    @allure.title("Адрес с пробелами в обязательных полях не сохраняется")
    def test_save_delivery_address_with_whitespace_fields(
        self, checkout_with_product
    ):
        checkout_page = checkout_with_product

        logger.info("Проверка сохранения адреса с пробелами в обязательных полях")
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Открыть форму адреса, если она закрыта"):
            if not checkout_page.address_form.is_visible():
                checkout_page.toggle_address_form()

        with allure.step("Проверить отображение формы"):
            expect(checkout_page.address_form).to_be_visible()

        logger.info("Заполнить обязательные поля только пробелами")

        with allure.step("Заполнить поля адреса пробелами"):
            checkout_page.fill_delivery_address(
                city="   ",
                street="   ",
                building="   ",
                apartment="   ",
                recipient="   ",
                phone="   "
            )

        logger.info("Нажать кнопку «Сохранить адрес»")

        with allure.step("Получить количество адресов до сохранения"):
            addresses_before = checkout_page.address_options.count()

        with allure.step("Проверить доступность кнопки сохранения"):
            expect(checkout_page.save_address_button).to_be_enabled()

        with allure.step("Попробовать сохранить адрес"):
            checkout_page.save_delivery_address()

        with allure.step("Проверить отображение ошибки"):
            expect(checkout_page.toast).to_be_visible()
            expect(checkout_page.toast).to_have_attribute(
                "data-toast-type", "error"
            )
            expect(checkout_page.toast).to_have_text("city обязателен")

        with allure.step("Проверить, что новый адрес не сохранился"):
            expect(checkout_page.address_options).to_have_count(
                addresses_before
            )

        with allure.step("Проверить, что форма адреса осталась открытой"):
            expect(checkout_page.address_form).to_be_visible()

    @allure.title("Нельзя перейти к оплате без адреса доставки")
    def test_cannot_proceed_to_payment_without_delivery_address(
        self, checkout_new_user
    ):
        checkout_page = checkout_new_user

        logger.info(
            "Проверка невозможности перехода к оплате без адреса доставки"
        )

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        logger.info("Проверяем отсутствие сохранённых адресов")

        with allure.step("Проверить отсутствие сохранённых адресов"):
            expect(checkout_page.address_options).to_have_count(0)

        logger.info("Проверяем, что кнопка «К оплате» неактивна")

        with allure.step("Проверить недоступность кнопки «К оплате»"):
            expect(checkout_page.pay_button).to_be_disabled()

@allure.epic("Интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Расчёт стоимости заказа и доставки")
class TestCheckoutTotal:

    @allure.title("Пересчёт стоимости доставки при смене способа получения")
    def test_delivery_fee_changes_when_switching_methods(
        self, checkout_with_product
    ):
        checkout_page = checkout_with_product

        logger.info(
            "Проверка пересчёта стоимости доставки "
            "при переключении способов получения"
        )
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Проверить стоимость курьерской доставки"):
            expect(checkout_page.delivery_fee).to_have_attribute(
                "data-cents", "29900"
            )

        logger.info("Переключиться на самовывоз")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить, что самовывоз бесплатный"):
            expect(checkout_page.delivery_fee).to_have_attribute(
                "data-cents", "0"
            )

        logger.info("Повторно выбрать способ доставки «Курьер»")

        with allure.step("Повторно выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Проверить восстановление стоимости доставки"):
            expect(checkout_page.delivery_fee).to_have_attribute(
                "data-cents", "29900"
            )

    @allure.title("Расчёт итоговой стоимости при курьерской доставке")
    def test_checkout_total_with_courier_delivery(
        self, checkout_with_product
    ):
        checkout_page = checkout_with_product

        logger.info(
            "Проверка расчёта итоговой стоимости заказа "
            "при курьерской доставке"
        )

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        logger.info("Получить стоимость товаров")

        with allure.step("Получить стоимость товаров в копейках"):
            subtotal = checkout_page.subtotal.inner_text()
            subtotal = int(float(
                subtotal.replace("\xa0", "")
                .replace(" ", "")
                .replace("$", "")
                .replace(",", ".")
            ) * 100)

        logger.info("Получить стоимость доставки")

        with allure.step("Получить стоимость доставки"):
            delivery_fee = int(
                checkout_page.delivery_fee.get_attribute("data-cents")
            )

        logger.info("Получить итоговую стоимость")

        with allure.step("Получить итоговую стоимость заказа"):
            total = checkout_page.total.inner_text()
            total = int(float(
                total.replace("\xa0", "")
                .replace(" ", "")
                .replace("$", "")
                .replace(",", ".")
            ) * 100)

        logger.info("Проверить информацию о скидках на странице")

        with allure.step("Получить информацию со страницы заказа"):
            logger.info(
                checkout_page.page.locator("body").inner_text()
            )

        logger.info("Вычислить ожидаемую итоговую стоимость")

        with allure.step("Рассчитать ожидаемую итоговую стоимость"):
            expected_total = subtotal + delivery_fee

        logger.info("Сравнить ожидаемую и фактическую стоимость")

        with allure.step("Проверить правильность итоговой стоимости"):
            assert total == expected_total, (
                f"Неверная итоговая стоимость: "
                f"ожидалось {expected_total}, получено {total}"
            )

    @allure.title("Расчёт итоговой стоимости при самовывозе")
    def test_checkout_total_with_pickup_delivery(
        self, checkout_with_product
    ):
        checkout_page = checkout_with_product

        logger.info(
            "Проверка расчёта итоговой стоимости заказа при самовывозе"
        )

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        logger.info("Получить стоимость товаров")

        with allure.step("Получить стоимость товаров в копейках"):
            subtotal = checkout_page.subtotal.inner_text()
            subtotal = int(float(
                subtotal.replace("\xa0", "")
                .replace(" ", "")
                .replace("$", "")
                .replace(",", ".")
            ) * 100)

        logger.info("Получить стоимость доставки")

        with allure.step("Получить стоимость доставки"):
            delivery_fee = int(
                checkout_page.delivery_fee.get_attribute("data-cents")
            )

        logger.info("Получить итоговую стоимость")

        with allure.step("Получить итоговую стоимость заказа"):
            total = checkout_page.total.inner_text()
            total = int(float(
                total.replace("\xa0", "")
                .replace(" ", "")
                .replace("$", "")
                .replace(",", ".")
            ) * 100)

        logger.info("Проверить, что самовывоз бесплатный")

        with allure.step("Проверить нулевую стоимость доставки"):
            assert delivery_fee == 0, (
                f"Ожидалась бесплатная доставка, получено {delivery_fee}"
            )

        logger.info("Проверить правильность итоговой стоимости")

        with allure.step("Рассчитать ожидаемую итоговую стоимость"):
            expected_total = subtotal + delivery_fee

        with allure.step("Сравнить ожидаемую и фактическую стоимость"):
            assert total == expected_total, (
                f"Неверная итоговая стоимость: "
                f"ожидалось {expected_total}, получено {total}"
            )

@allure.epic("Интернет-магазин")
@allure.feature("Оформление заказа")
@allure.story("Переходы между этапами оформления заказа")
class TestCheckoutNavigation:

    @allure.title("Переход к оплате при самовывозе")
    def test_proceed_to_payment_with_pickup(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест выбора опций самовывоза")
        logger.info("Выбрать способ доставки «Самовывоз»")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить отображение пунктов самовывоза"):
            expect(checkout_page.pickup_options.first).to_be_visible()

        logger.info("Выбор пункта выдачи")

        with allure.step("Выбрать первый пункт выдачи"):
            checkout_page.select_pickup_point(index=0)

        with allure.step("Проверить активность выбранного пункта выдачи"):
            expect(checkout_page.pickup_options.nth(0)).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Перейти на страницу оплаты")

        with allure.step("Проверить доступность кнопки перехода к оплате"):
            expect(checkout_page.pay_button).to_be_enabled()

        with allure.step("Перейти на страницу оплаты"):
            checkout_page.proceed_to_payment()

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

    @allure.title("Переход к оплате при курьерской доставке")
    def test_proceed_to_payment_with_courier(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест перехода к оплате при курьерской доставке")
        logger.info("Выбрать способ доставки «Курьер»")

        with allure.step("Выбрать курьерскую доставку"):
            checkout_page.select_courier_delivery()

        with allure.step("Проверить активность курьерской доставки"):
            expect(checkout_page.courier_button).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Выбрать первый сохранённый адрес доставки")

        with allure.step("Проверить наличие сохранённого адреса"):
            expect(checkout_page.address_options.first).to_be_visible()

        with allure.step("Выбрать первый сохранённый адрес"):
            checkout_page.address_options.first.click()

        with allure.step("Проверить активность выбранного адреса"):
            expect(checkout_page.address_options.first).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Перейти на страницу оплаты")

        with allure.step("Проверить доступность кнопки перехода к оплате"):
            expect(checkout_page.pay_button).to_be_enabled()

        with allure.step("Перейти на страницу оплаты"):
            checkout_page.proceed_to_payment()

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

    @allure.title("Возврат с оплаты к выбору доставки")
    def test_return_to_delivery_from_payment(self, checkout_with_product):
        checkout_page = checkout_with_product

        logger.info("Начинаем тест возврата с этапа оплаты к выбору доставки")
        logger.info("Выбрать способ доставки «Самовывоз»")

        with allure.step("Выбрать самовывоз"):
            checkout_page.select_pickup_delivery()

        with allure.step("Проверить отображение пунктов самовывоза"):
            expect(checkout_page.pickup_options.first).to_be_visible()

        logger.info("Выбор пункта выдачи")

        with allure.step("Выбрать первый пункт выдачи"):
            checkout_page.select_pickup_point(index=0)

        with allure.step("Проверить активность выбранного пункта выдачи"):
            expect(checkout_page.pickup_options.nth(0)).to_have_attribute(
                "data-active", "true"
            )

        logger.info("Перейти на страницу оплаты")

        with allure.step("Проверить доступность кнопки перехода к оплате"):
            expect(checkout_page.pay_button).to_be_enabled()

        with allure.step("Перейти на страницу оплаты"):
            checkout_page.proceed_to_payment()

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Нажать кнопку возврата к выбору доставки")

        with allure.step("Вернуться к выбору доставки"):
            checkout_page.return_to_delivery()

        with allure.step("Проверить отображение страницы доставки"):
            expect(
                checkout_page.page.get_by_role("heading", name="Доставка")
            ).to_be_visible()

        with allure.step("Проверить сохранение выбранного способа доставки"):
            expect(checkout_page.pickup_button).to_have_attribute(
                "data-active", "true"
            )

        with allure.step("Проверить сохранение выбранного пункта выдачи"):
            expect(checkout_page.pickup_options.nth(0)).to_have_attribute(
                "data-active", "true"
            )

@allure.epic("Интернет-магазин")
@allure.feature("Оплата заказа")
@allure.story("Оплата банковской картой и 3D Secure")
class TestPayment:

    @allure.title("Отображение формы оплаты банковской картой")
    def test_payment_form_displayed(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест отображения формы оплаты банковской картой")
        logger.info("Проверить отображение заголовка «Оплата»")

        with allure.step("Проверить заголовок страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Проверить отображение формы оплаты")

        with allure.step("Проверить отображение формы и полей банковской карты"):
            expect(checkout_page.card_form).to_be_visible()
            expect(checkout_page.card_pan).to_be_visible()
            expect(checkout_page.card_expiry).to_be_visible()
            expect(checkout_page.card_cvc).to_be_visible()
            expect(checkout_page.card_holder).to_be_visible()
            expect(checkout_page.submit_payment_button).to_be_visible()
            expect(checkout_page.card_visual).to_be_visible()

    @allure.title("Ввод корректных данных банковской карты")
    def test_fill_payment_form_with_valid_card(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест ввода корректных данных банковской карты")
        logger.info("Ввести номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Проверить введённые данные банковской карты")

        with allure.step("Проверить введённые данные"):
            expect(checkout_page.card_pan).to_have_value(
                "4111 1111 1111 1111"
            )
            expect(checkout_page.card_expiry).to_have_value("12/28")
            expect(checkout_page.card_cvc).to_have_value("123")
            expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

        logger.info("Проверить, что форма оплаты отображается")

        with allure.step("Проверить отображение формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

        logger.info("Проверить, что кнопка оплаты отображается")

        with allure.step("Проверить отображение кнопки оплаты"):
            expect(checkout_page.submit_payment_button).to_be_visible()

    @allure.title("Оплата с пустыми полями банковской карты")
    def test_payment_with_empty_card_fields(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест оплаты с пустыми полями банковской карты")
        logger.info("Проверить, что форма оплаты отображается")

        with allure.step("Проверить отображение формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

        logger.info("Очистить все поля банковской карты")

        with allure.step("Очистить поля банковской карты"):
            checkout_page.card_pan.fill("")
            checkout_page.card_expiry.fill("")
            checkout_page.card_cvc.fill("")
            checkout_page.card_holder.fill("")

        logger.info("Проверить, что все поля банковской карты пустые")

        with allure.step("Проверить пустые поля"):
            expect(checkout_page.card_pan).to_be_empty()
            expect(checkout_page.card_expiry).to_be_empty()
            expect(checkout_page.card_cvc).to_be_empty()
            expect(checkout_page.card_holder).to_be_empty()

        logger.info("Проверить, что кнопка оплаты отображается")

        with allure.step("Проверить отображение кнопки оплаты"):
            expect(checkout_page.submit_payment_button).to_be_visible()

        logger.info("Нажать кнопку «Оплатить» с пустыми полями")

        with allure.step("Попытаться оплатить заказ с пустыми полями"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить, что пользователь остался на этапе оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Проверить, что форма оплаты осталась доступна")

        with allure.step("Проверить доступность формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Оплата с некорректным номером банковской карты")
    def test_payment_with_invalid_card_number(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест оплаты с некорректным номером банковской карты")
        logger.info("Ввести некорректный номер банковской карты")

        with allure.step("Ввести некорректный номер карты"):
            checkout_page.card_pan.fill("1234567890123456")

        logger.info("Заполнить остальные поля корректными данными")

        with allure.step("Заполнить остальные поля карты"):
            checkout_page.card_expiry.fill("12/28")
            checkout_page.card_cvc.fill("123")
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Проверить, что данные введены")

        with allure.step("Проверить введённые данные"):
            expect(checkout_page.card_pan).to_have_value(
                "1234 5678 9012 3456"
            )
            expect(checkout_page.card_expiry).to_have_value("12/28")
            expect(checkout_page.card_cvc).to_have_value("123")
            expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

        logger.info("Попытаться оплатить заказ с некорректным номером карты")

        with allure.step("Попытаться оплатить заказ"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить, что оплата не выполнена"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Оплата картой с истёкшим сроком действия")
    def test_payment_with_expired_card(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест оплаты с истёкшим сроком действия карты")
        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести истёкший срок действия карты")

        with allure.step("Ввести истёкший срок действия карты"):
            checkout_page.card_expiry.fill("12/24")

        logger.info("Ввести корректный CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Проверить введённые данные банковской карты")

        with allure.step("Проверить введённые данные"):
            expect(checkout_page.card_pan).to_have_value(
                "4111 1111 1111 1111"
            )
            expect(checkout_page.card_expiry).to_have_value("12/24")
            expect(checkout_page.card_cvc).to_have_value("123")
            expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

        logger.info("Попытаться оплатить заказ с просроченной картой")

        with allure.step("Попытаться оплатить заказ"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить, что оплата не выполнена"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Оплата с некорректным CVC")
    def test_payment_with_invalid_cvc(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест оплаты с некорректным CVC")
        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести корректный срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести некорректный CVC")

        with allure.step("Ввести некорректный CVC"):
            checkout_page.card_cvc.fill("12")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Проверить введённые данные банковской карты")

        with allure.step("Проверить введённые данные"):
            expect(checkout_page.card_pan).to_have_value(
                "4111 1111 1111 1111"
            )
            expect(checkout_page.card_expiry).to_have_value("12/28")
            expect(checkout_page.card_cvc).to_have_value("12")
            expect(checkout_page.card_holder).to_have_value("IVAN IVANOV")

        logger.info("Попытаться оплатить заказ с некорректным CVC")

        with allure.step("Попытаться оплатить заказ"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить, что оплата не выполнена"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Проверка итоговой стоимости на этапе оплаты")
    def test_order_total_on_payment_step(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест проверки итоговой стоимости заказа на этапе оплаты")
        logger.info("Проверить, что пользователь находится на этапе оплаты")

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Проверить отображение стоимости товаров")

        with allure.step("Проверить отображение стоимости товаров"):
            expect(checkout_page.subtotal).to_be_visible()

        logger.info("Проверить отображение стоимости доставки")

        with allure.step("Проверить отображение стоимости доставки"):
            expect(checkout_page.delivery_fee).to_be_visible()

        logger.info("Проверить отображение итоговой стоимости заказа")

        with allure.step("Проверить отображение итоговой стоимости"):
            expect(checkout_page.total).to_be_visible()

        logger.info("Получить стоимость товаров, доставки и итоговую сумму")

        with allure.step("Получить суммы заказа"):
            subtotal = checkout_page.subtotal.inner_text()
            delivery_fee = checkout_page.delivery_fee.inner_text()
            total = checkout_page.total.inner_text()

        logger.info(f"Стоимость товаров: {subtotal}")
        logger.info(f"Стоимость доставки: {delivery_fee}")
        logger.info(f"Итоговая стоимость: {total}")

        logger.info("Проверить, что стоимость доставки при самовывозе равна нулю")

        with allure.step("Проверить стоимость заказа при самовывозе"):
            assert checkout_page.delivery_fee.get_attribute("data-cents") == "0"
            assert total == subtotal

    @allure.title("Успешная оплата заказа банковской картой")
    def test_successful_payment_with_valid_card(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест успешной оплаты заказа банковской картой")
        logger.info("Проверить, что пользователь находится на этапе оплаты")

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести корректный срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести корректный CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Нажать кнопку «Оплатить»")

        with allure.step("Нажать кнопку оплаты"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить появление окна 3D Secure")

        with allure.step("Проверить появление окна 3D Secure"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Получить тестовый SMS-код")

        with allure.step("Получить тестовый SMS-код"):
            otp_code = checkout_page.threeds_otp_hint.get_attribute("data-otp")
            assert otp_code is not None, "Не удалось получить SMS-код"

        logger.info("Ввести SMS-код подтверждения")

        with allure.step("Ввести SMS-код подтверждения"):
            checkout_page.threeds_otp.fill(otp_code)

        logger.info("Проверить, что кнопка подтверждения активна")

        with allure.step("Проверить доступность кнопки подтверждения"):
            expect(checkout_page.threeds_confirm_button).to_be_enabled()

        logger.info("Подтвердить оплату")

        with allure.step("Подтвердить оплату"):
            checkout_page.threeds_confirm_button.click()

        logger.info("Проверить закрытие окна 3D Secure")

        with allure.step("Проверить завершение оплаты"):
            expect(checkout_page.threeds_modal).not_to_be_visible()
            expect(checkout_page.card_form).not_to_be_visible()

    @allure.title("Оплата с некорректным кодом 3D Secure")
    def test_payment_with_invalid_3ds_code(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест оплаты с некорректным кодом 3D Secure")
        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести корректный срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести корректный CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Нажать кнопку «Оплатить»")

        with allure.step("Нажать кнопку оплаты"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить появление окна 3D Secure")

        with allure.step("Проверить появление окна 3D Secure"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Получить корректный SMS-код")

        with allure.step("Получить корректный SMS-код"):
            correct_otp = checkout_page.threeds_otp_hint.get_attribute(
                "data-otp"
            )
            assert correct_otp is not None, "Не удалось получить SMS-код"

        logger.info("Сформировать некорректный SMS-код")

        with allure.step("Сформировать некорректный SMS-код"):
            invalid_otp = "000000" if correct_otp != "000000" else "111111"

        logger.info("Ввести некорректный SMS-код")

        with allure.step("Ввести некорректный SMS-код"):
            checkout_page.threeds_otp.fill(invalid_otp)

        logger.info("Проверить, что кнопка подтверждения активна")

        with allure.step("Проверить доступность кнопки подтверждения"):
            expect(checkout_page.threeds_confirm_button).to_be_enabled()

        logger.info("Подтвердить оплату с некорректным SMS-кодом")

        with allure.step("Подтвердить оплату с неверным кодом"):
            checkout_page.threeds_confirm_button.click()

        logger.info("Проверить, что окно 3D Secure осталось открытым")

        with allure.step("Проверить, что окно 3D Secure осталось открытым"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить доступность формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Подтверждение оплаты с пустым кодом 3D Secure")
    def test_payment_with_empty_3ds_code(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест подтверждения оплаты с пустым SMS-кодом")
        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести корректный срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести корректный CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Нажать кнопку «Оплатить»")

        with allure.step("Нажать кнопку оплаты"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить появление окна 3D Secure")

        with allure.step("Проверить появление окна 3D Secure"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Проверить, что поле SMS-кода пустое")

        with allure.step("Проверить пустое поле SMS-кода"):
            expect(checkout_page.threeds_otp).to_be_empty()

        logger.info("Проверить, что кнопка подтверждения неактивна")

        with allure.step("Проверить недоступность кнопки подтверждения"):
            expect(checkout_page.threeds_confirm_button).to_be_disabled()

        logger.info("Проверить, что окно 3D Secure осталось открытым")

        with allure.step("Проверить отображение окна 3D Secure"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Проверить, что форма оплаты остаётся доступной")

        with allure.step("Проверить доступность формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

    @allure.title("Отмена оплаты через 3D Secure")
    def test_cancel_3ds_payment(self, payment_with_product):
        checkout_page = payment_with_product

        logger.info("Начинаем тест отмены оплаты через 3D Secure")
        logger.info("Ввести корректный номер банковской карты")

        with allure.step("Ввести номер банковской карты"):
            checkout_page.card_pan.fill("4111111111111111")

        logger.info("Ввести корректный срок действия карты")

        with allure.step("Ввести срок действия карты"):
            checkout_page.card_expiry.fill("12/28")

        logger.info("Ввести корректный CVC")

        with allure.step("Ввести CVC"):
            checkout_page.card_cvc.fill("123")

        logger.info("Ввести имя владельца карты")

        with allure.step("Ввести имя владельца карты"):
            checkout_page.card_holder.fill("IVAN IVANOV")

        logger.info("Нажать кнопку «Оплатить»")

        with allure.step("Нажать кнопку оплаты"):
            checkout_page.submit_payment_button.click()

        logger.info("Проверить появление окна 3D Secure")

        with allure.step("Проверить появление окна 3D Secure"):
            expect(checkout_page.threeds_modal).to_be_visible()

        logger.info("Проверить отображение кнопки «Отмена»")

        with allure.step("Проверить отображение кнопки отмены"):
            expect(checkout_page.threeds_cancel_button).to_be_visible()

        logger.info("Нажать кнопку «Отмена»")

        with allure.step("Отменить оплату"):
            checkout_page.threeds_cancel_button.click()

        logger.info("Проверить закрытие окна 3D Secure")

        with allure.step("Проверить закрытие окна 3D Secure"):
            expect(checkout_page.threeds_modal).not_to_be_visible()

        logger.info("Проверить, что пользователь остался на этапе оплаты")

        with allure.step("Проверить отображение страницы оплаты"):
            expect(
                checkout_page.page.get_by_role("heading", name="Оплата")
            ).to_be_visible()

        logger.info("Проверить, что форма оплаты осталась доступна")

        with allure.step("Проверить доступность формы оплаты"):
            expect(checkout_page.card_form).to_be_visible()

        logger.info("Проверить, что кнопка оплаты снова активна")

        with allure.step("Проверить доступность кнопки оплаты"):
            expect(checkout_page.submit_payment_button).to_be_enabled()