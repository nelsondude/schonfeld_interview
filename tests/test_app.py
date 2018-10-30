import json

import falcon

from api import orders_util

TEST_ORDER = \
    {
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


def test_post_order(client):
    response = client.simulate_post(
        '/orders',
        body=json.dumps(TEST_ORDER),
    )
    assert response.status == falcon.HTTP_200
    assert 'trader_id' in response.json['data']


def test_write_to_file(fake_trade_file):
    orders, trader_id = TEST_ORDER['orders'], TEST_ORDER['trader_id']
    orders_util.writeToTradesFile(trader_id, orders)
    with open(fake_trade_file, 'r') as f:
        for i, line in enumerate(f):
            assert all(str(el) in line for el in orders[i].values())  # all values in the file
            assert line.startswith(trader_id)
