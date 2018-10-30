import falcon
import json
import pytest
from falcon import testing

from api.app import APP


@pytest.fixture
def client():
    return testing.TestClient(APP)


def test_post_order(client):
    order = {
        'trader_id': '12345',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 100,
                'orderType': 'sell'
            }
        ]
    }
    response = client.simulate_post(
        '/orders',
        body=json.dumps(order),
    )
    assert response.status == falcon.HTTP_200
    assert 'trader_id' in response.json['data']
