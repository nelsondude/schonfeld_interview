import falcon
from api.orders import *
from .health_check import HealthCheck

APP = falcon.API()

health_check_resource = HealthCheck()
APP.add_route('/health', health_check_resource)

# API Routes Below
trader_orders_resource = TraderOrders()
APP.add_route('/orders/{trader_id}', trader_orders_resource)

order_resource = Orders()
APP.add_route('/orders', order_resource)

