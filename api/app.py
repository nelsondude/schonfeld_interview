import falcon
from api.orders import Orders
from .health_check import HealthCheck

APP = falcon.API()

health_check_resource = HealthCheck()
APP.add_route('/health', health_check_resource)

# API Routes Below
order_resource = Orders()
APP.add_route('/orders', order_resource)

