import pytest
from unittest.mock import patch, Mock

from external_api import convert_transaction_to_rub


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

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_convert_transaction_usd_success(self, mock_getenv, mock_requests_get):
        """Тест успешной конвертации USD в рубли."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 75.5}
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 7550.0
        mock_requests_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            headers={"apikey": "test_api_key"},
            params={"symbols": "RUB", "base": "USD"},
            timeout=10
        )

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_convert_transaction_eur_success(self, mock_getenv, mock_requests_get):
        """Тест успешной конвертации EUR в рубли."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 82.3}
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "50.75",
                "currency": {"code": "EUR"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == pytest.approx(4176.725, rel=1e-9)
        mock_requests_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            headers={"apikey": "test_api_key"},
            params={"symbols": "RUB", "base": "EUR"},
            timeout=10
        )

    @patch("external_api.os.getenv")
    def test_convert_transaction_no_api_key(self, mock_getenv):
        """Тест случая, когда API ключ не найден."""
        mock_getenv.return_value = None

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0
        mock_getenv.assert_called_once_with("EXCHANGE_RATES_API_KEY")

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_convert_transaction_api_error(self, mock_getenv, mock_requests_get):
        """Тест случая, когда API возвращает ошибку."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "error": "Invalid API key"
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_convert_transaction_request_exception(self, mock_getenv, mock_requests_get):
        """Тест случая, когда происходит ошибка при запросе."""
        from requests.exceptions import RequestException

        mock_getenv.return_value = "test_api_key"
        mock_requests_get.side_effect = RequestException("Connection error")

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_transaction_to_rub(transaction)

        assert result == 0.0

    @patch("external_api.requests.get")
    @patch("external_api.os.getenv")
    def test_convert_transaction_json_error(self, mock_getenv, mock_requests_get):
        """Тест случая, когда ответ API некорректный."""
        mock_getenv.return_value = "test_api_key"
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

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
