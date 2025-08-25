import pytest

import requests


from unittest.mock import Mock, patch
from external_api import get_exchange_rate, convert_transaction_to_rub


class TestGetExchangeRate:
    """Тесты для функции get_exchange_rate."""

    @patch("external_api.os.getenv")
    def test_get_exchange_rate_no_api_key(self, mock_getenv):
        """Тест случая, когда API ключ не найден."""
        mock_getenv.return_value = None

        result = get_exchange_rate("USD")

        assert result is None
        mock_getenv.assert_called_once_with("EXCHANGE_RATES_API_KEY")

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_get_exchange_rate_success(self, mock_getenv, mock_requests_get):
        """Тест успешного получения курса валюты."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 75.5}
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        result = get_exchange_rate("USD")

        assert result == 75.5
        mock_requests_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            headers={"apikey": "test_api_key"},
            params={"symbols": "RUB", "base": "USD"},
            timeout=10
        )

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_get_exchange_rate_api_error(self, mock_getenv, mock_requests_get):
        """Тест случая, когда API возвращает ошибку."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "error": "Invalid API key"
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        result = get_exchange_rate("USD")

        assert result is None

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_get_exchange_rate_request_exception(self, mock_getenv, mock_requests_get):
        """Тест случая, когда происходит ошибка при запросе."""
        mock_getenv.return_value = "test_api_key"
        mock_requests_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = get_exchange_rate("USD")

        assert result is None

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_get_exchange_rate_json_error(self, mock_getenv, mock_requests_get):
        """Тест случая, когда ответ API некорректный."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        result = get_exchange_rate("USD")

        assert result is None


class TestConvertTransactionToRub:
    """Тесты для функции convert_transaction_to_rub."""

    def test_convert_transaction_rub_currency(self):
        """Тест конвертации транзакции в рублях."""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 1000.5

    @patch("external_api.get_exchange_rate")
    def test_convert_transaction_usd_success(self, mock_get_exchange_rate):
        """Тест успешной конвертации USD в рубли."""
        mock_get_exchange_rate.return_value = 75.5

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 7550.0
        mock_get_exchange_rate.assert_called_once_with("USD")

    @patch("external_api.get_exchange_rate")
    def test_convert_transaction_eur_success(self, mock_get_exchange_rate):
        """Тест успешной конвертации EUR в рубли."""
        mock_get_exchange_rate.return_value = 82.3

        transaction = {
            "operationAmount": {
                "amount": "50.75",
                "currency": {"code": "EUR"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 4176.725
        mock_get_exchange_rate.assert_called_once_with("EUR")

    @patch("external_api.get_exchange_rate")
    def test_convert_transaction_api_error(self, mock_get_exchange_rate):
        """Тест случая, когда API возвращает ошибку."""
        mock_get_exchange_rate.return_value = None

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    def test_convert_transaction_unsupported_currency(self):
        """Тест конвертации неподдерживаемой валюты."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "GBP"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    def test_convert_transaction_invalid_structure(self):
        """Тест обработки некорректной структуры транзакции."""
        transaction = {
            "invalid": "structure"
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    def test_convert_transaction_missing_amount(self):
        """Тест случая отсутствия суммы в транзакции."""
        transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    def test_convert_transaction_missing_currency(self):
        """Тест случая отсутствия валюты в транзакции."""
        transaction = {
            "operationAmount": {
                "amount": "100"
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 100.0  # По умолчанию RUB

    def test_convert_transaction_empty(self):
        """Тест пустой транзакции."""
        transaction = {}

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0
