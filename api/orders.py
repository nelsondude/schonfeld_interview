import falcon

from .orders_util import Trade


class Orders:

    def on_post(self, request, response):
        trader_id = request.media.get('trader_id')
        orders = request.media.get('orders')
        t = Trade(trader_id)
        t.write_to_trades_file(orders)
        response.media = {
            'data': {
                'trader_id': trader_id,
                'orders': orders
            }
        }
        response.status = falcon.HTTP_200


class TraderOrders:
    def on_get(self, request, response, trader_id):
        t = Trade(trader_id)
        trades = t.get_trades_for_trader()
        response.media = {
            'data': trades
        }
        response.status = falcon.HTTP_200
