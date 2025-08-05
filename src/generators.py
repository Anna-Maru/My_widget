from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict], target_code: str) -> Iterator[Dict]:
    """
    Генератор из списка транзакций возвращает только те операции,
    у которых в operationAmount.currency.code содержится заданный target_code.
    """
    for txn in transactions:
        amount = txn.get("operationAmount", {})
        currency = amount.get("currency", {})
        code = currency.get("code")
        if code == target_code:
            yield txn


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор принимает список транзакций и поочередно
    возвращает значение поля 'description' каждой операции,
    если это поле существует.
    """
    for txn in transactions:
        desc = txn.get("description")
        if desc is not None:
            yield desc


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров карт в формате 'XXXX XXXX XXXX XXXX',
    начиная со start и до end включительно.
    Номера представлены 16-значными строками с лидирующими нулями.
    Рекомендуются диапазоны от 1 до 9999999999999999.
    """
    for num in range(start, end + 1):
        s = str(num).rjust(16, '0')
        yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
