from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub, get_amount_in_rub


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_key")


@pytest.fixture(autouse=True)
def load_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_key")


def test_convert_to_rub_usd_success():
    with patch("src.external_api.requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"success": True, "result": 1234.56}
        mock_get.return_value = mock_resp

        result = convert_to_rub(10.0, "USD")
        assert result == 1234.56
        mock_get.assert_called_once()


def test_convert_to_rub_calls_api(monkeypatch):
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"success": True, "result": 1500.5}
    monkeypatch.setattr("src.external_api.requests.get", lambda *args, **kwargs: mock_resp)

    result = convert_to_rub(10.0, "USD")
    assert result == 1500.5


def test_convert_to_rub_no_key(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="API_KEY is missing"):
        convert_to_rub(5, "EUR")


@pytest.mark.parametrize("currency, amount, expected", [
    ("RUB", 300, 300),
    ("GBP", 450.75, 450.75),
])
def test_get_amount_in_rub_non_convert(currency, amount, expected):
    txn = {"operationAmount": {"amount": "300", "currency": {"code": "RUB"}}}
    assert get_amount_in_rub(txn) == 300.0


def test_get_amount_in_rub_usd(monkeypatch):
    txn = {"operationAmount": {"amount": "450.75", "currency": {"code": "GBP"}}}
    monkeypatch.setattr("src.external_api.convert_to_rub", lambda amt, cur: 999.99)
    assert get_amount_in_rub(txn) == 999.99


def test_get_amount_in_rub_invalid_amount():
    txn = {"operationAmount": {"amount": "not_num", "currency": {"code": "RUB"}}}
    assert get_amount_in_rub(txn) == 0.0
