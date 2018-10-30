import json

import falcon

from api import orders_util

TEST_ORDER = \
    {
        'trader_id': 'jill',
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


TEST_ORDER2 = \
    {
        'trader_id': 'bob',
        'orders': [
            {
                'symbol': 'MDB',
                'quantity': 200,
                'orderType': 'sell'
            },
            {
                'symbol': 'MSFT',
                'quantity': 200,
                'orderType': 'sell'
            }
        ]
    }


def test_post_order(client):
    response = client.simulate_post(
        '/orders',
        body=json.dumps(TEST_ORDER),
    )
    assert response.status == falcon.HTTP_200
    assert TEST_ORDER == response.json['data']


def test_write_to_file(fake_trade_file):
    orders, trader_id = TEST_ORDER['orders'], TEST_ORDER['trader_id']
    orders_util.writeToTradesFile(trader_id, orders)
    with open(fake_trade_file, 'r') as f:
        for i, line in enumerate(f):
            assert all(str(el) in line for el in orders[i].values())  # all values in the file
            assert line.startswith(trader_id)


def test_get_trader_id_trades():
    orders_util.writeToTradesFile(TEST_ORDER['trader_id'], TEST_ORDER['orders'])
    orders_util.writeToTradesFile(TEST_ORDER2['trader_id'], TEST_ORDER2['orders'])
    trades = orders_util.getTradesForTrader(TEST_ORDER2['trader_id'])
    assert all(trade['symbol'] == TEST_ORDER2['orders'][i]['symbol']
               for i, trade in enumerate(trades))


def test_get_trades_view(client):
    client.simulate_post(
        '/orders',
        body=json.dumps(TEST_ORDER),
    )
    response = client.simulate_get(
        '/orders/{}'.format(TEST_ORDER['trader_id'])
    )
    assert response.status == falcon.HTTP_200


