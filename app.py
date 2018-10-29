import falcon
from health_check import HealthCheck

APP = falcon.API()

health_check_resource = HealthCheck()
APP.add_route('/health', health_check_resource)

