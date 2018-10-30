import falcon
import json
import pytest
from falcon import testing

from api.app import APP
import api.orders_util


@pytest.fixture
def client():
    return testing.TestClient(APP)


@pytest.fixture(autouse=True)  # apply to all tests
def fake_trade_file(tmpdir, monkeypatch):
    p = tmpdir.mkdir('test_data').join('trades.csv')
    monkeypatch.setattr(api.orders_util, 'TRADES_FILE_PATH', str(p))
    return p


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
