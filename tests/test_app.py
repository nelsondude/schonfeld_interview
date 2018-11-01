import csv
import json

import falcon

from api.orders_util import Trade

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
    t = Trade(trader_id)
    t.writeToTradesFile(orders)
    with open(fake_trade_file, 'r') as f:
        for i, line in enumerate(f):
            assert all(str(el) in line for el in orders[i].values())  # all values in the file
            assert line.startswith(trader_id)


def test_get_trader_id_trades():
    t1 = Trade(TEST_ORDER['trader_id'])
    t2 = Trade(TEST_ORDER2['trader_id'])
    t1.writeToTradesFile(TEST_ORDER['orders'])
    t2.writeToTradesFile(TEST_ORDER2['orders'])
    trades = t2.getTradesForTrader()
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


def test_get_trades_to_update(fake_trade_file):
    with open(fake_trade_file, 'w', newline='') as f:
        row = 'misty;AAPL;80;sell;2018-11-01 15:48:14.605383;open'
        writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row.split(';'))

    t = Trade('bob')
    trades = t.getUpdateTrades('AAPL', 80, 'buy')
    assert trades == {('misty', '2018-11-01 15:48:14.605383'): 80}


def test_updated_trade_file(client, fake_trade_file):
    client.simulate_post(
        '/orders',
        body=json.dumps(TEST_ORDER),
    )
    client.simulate_post(
        '/orders',
        body=json.dumps(TEST_ORDER2),
    )
    with open(fake_trade_file, 'r') as f:
        # Test that one of the buy lines became filled
        assert any(line.startswith('jill;MSFT;200;buy;') and line.endswith('filled\n') for line in f)
