import pytest
from falcon import testing

import api.orders_util
from api.app import APP


@pytest.fixture
def client():
    return testing.TestClient(APP)


@pytest.fixture(autouse=True)  # apply to all tests
def fake_trade_file(tmpdir, monkeypatch):
    p = tmpdir.mkdir('test_data').join('trades.csv')
    monkeypatch.setattr(api.orders_util, 'TRADES_FILE_PATH', str(p))
    return p