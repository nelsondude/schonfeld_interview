import falcon
from .orders_util import writeToTradesFile, getTradesForTrader


class Orders:

    def on_post(self, request, response):
        trader_id = request.media.get('trader_id')
        orders = request.media.get('orders')
        writeToTradesFile(trader_id, orders)
        response.media = {
            'data': {
                'trader_id': trader_id,
                'orders': orders
            }
        }
        response.status = falcon.HTTP_200


class TraderOrders:
    def on_get(self, request, response, trader_id):
        trades = getTradesForTrader(trader_id)
        response.media = {
            'data': trades
        }
        response.status = falcon.HTTP_200
