import falcon, json


class Orders:

    def on_get(self, request, response):
        response.media = {}
        response.statis = falcon.HTTP_200

    def on_post(self, request, response):
        trader_id = request.media.get('trader_id')
        orders = request.media.get('orders')

        response.media = {
            'data': {
                'trader_id': trader_id,
                'orders': orders
            }
        }
        response.status = falcon.HTTP_200