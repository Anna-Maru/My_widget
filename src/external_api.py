import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму транзакции в рубли с использованием внешнего API."""
    if currency.upper() == "RUB":
        return float(amount)

    if not API_KEY:
        raise RuntimeError("API_KEY is missing.")

    headers = {"apikey": API_KEY}
    params = {"from": currency, "to": "RUB", "amount": str(amount)}
    resp = requests.get('https://api.apilayer.com/exchangerates_data/convert', headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return float(data.get("result", 0.0))


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    try:
        op = transaction.get("operationAmount", {})
        amount = float(op.get("amount", "0"))
        currency = op.get("currency", {}).get("code", "RUB")
    except (ValueError, TypeError):
        return 0.0

    return convert_to_rub(amount, currency)
