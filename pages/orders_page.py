import logging


logger = logging.getLogger(__name__)

class OrdersPage:
    def __init__(self, page):
        self.page = page
        self.url = "http://localhost:8081/#/orders"

        self.title = page.get_by_test_id("orders-title")
        self.subtitle = page.get_by_test_id("orders-subtitle")
        self.orders_page = page.get_by_test_id("orders-page")

        self.order_cards = page.get_by_test_id("order-card")
        self.order_status = page.get_by_test_id("order-status")
        self.order_items = page.get_by_test_id("order-items")
        self.order_item = page.get_by_test_id("order-item")

        self.delivery_method = page.get_by_test_id("order-delivery-method")
        self.delivery_info = page.get_by_test_id("order-delivery-info")
        self.delivery_fee = page.get_by_test_id("order-delivery-fee")

        self.order_total = page.get_by_test_id("order-total")
        self.placed_notice = page.get_by_test_id("orders-placed-notice")

    def open(self):
        logger.info("Открываем страницу заказов")
        self.page.goto(self.url)