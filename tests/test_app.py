import falcon
import json


def test_post_order(client):
    order = {
        'trader_id': '12345',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 100,
                'orderType': 'sell'
            },
            {
                'symbol': 'MSFT',
                'quantity': 200,
                'orderType': 'buy'
            }
        ]
    }
    response = client.simulate_post(
        '/orders',
        body=json.dumps(order),
    )
    assert response.status == falcon.HTTP_200
    assert 'trader_id' in response.json['data']
