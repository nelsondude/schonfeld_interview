import csv
import json

import falcon

from api.orders_util import Trade

TEST_ORDER = \
    {
        'trader_id': 'jill',
        'orders': [
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
    t.write_to_trades_file(orders)
    with open(fake_trade_file, 'r') as f:
        for i, line in enumerate(f):
            assert orders[i]['symbol'] in line
            assert str(orders[i]['quantity']) in line
            assert line.startswith(trader_id)


def test_get_trader_id_trades():
    t1 = Trade(TEST_ORDER['trader_id'])
    t2 = Trade(TEST_ORDER2['trader_id'])
    t1.write_to_trades_file(TEST_ORDER['orders'])
    t2.write_to_trades_file(TEST_ORDER2['orders'])
    trades = t2.get_trades_for_trader()
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
    f = open(fake_trade_file, 'w', newline='')
    row = 'misty;AAPL;80;80;sell;2018-11-01 18:52:17.685814'
    writer = csv.writer(f)
    writer.writerow([row])
    f.close()

    t = Trade('bob')
    trades = t.get_update_trades('AAPL', 80, 'buy')
    assert str(trades[0][0]).startswith('misty;AAPL;80')  # indicates the changed row


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
        assert any(line.startswith('jill;MSFT;200;0;') for line in f)  # 0 indicates that it is filled
