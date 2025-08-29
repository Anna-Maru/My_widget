import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com"


def convert_to_rub(amount: float, currency: str) -> float:
    headers = {"apikey": API_KEY} if API_KEY else {}
    params = {"from": currency, "to": "RUB", "amount": str(amount)}
    resp = requests.get(BASE_URL, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return float(data.get("result", 0.0))


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    op = transaction.get("operationAmount", {})
    try:
        amount = float(op.get("amount", "0"))
    except ValueError:
        return 0.0

    currency = op.get("currency", {}).get("code", "RUB")
    if currency in ("USD", "EUR"):
        return convert_to_rub(amount, currency)
    return amount
