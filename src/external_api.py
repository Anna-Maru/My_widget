import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    try:
        amount = float(transaction.get("operationAmount", {}).get("amount", 0))
        currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code", "RUB")

        if currency_code == "RUB":
            return amount

        if currency_code in ["USD", "EUR"]:
            api_key = os.getenv("API_KEY")
            if not api_key:
                print("Ошибка: API ключ не найден в переменных окружения")
                return 0.0

            url = "https://apilayer.com/exchangerates_data-api"

            headers = {
                "apikey": api_key
            }

            params = {
                "symbols": "RUB",
                "base": currency_code
            }

            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()

                if data.get("success") and "rates" in data and "RUB" in data["rates"]:
                    exchange_rate = float(data["rates"]["RUB"])
                    return amount * exchange_rate
                else:
                    print(f"Ошибка в ответе API: {data}")
                    return 0.0

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                return 0.0
            except (KeyError, ValueError, TypeError) as e:
                print(f"Ошибка при обработке ответа API: {e}")
                return 0.0

        print(f"Неподдерживаемая валюта: {currency_code}")
        return 0.0

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка при обработке транзакции: {e}")
        return 0.0
