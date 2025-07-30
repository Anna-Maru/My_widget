from typing import Dict, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


# Пример фикстуры с тестовыми транзакциями
@pytest.fixture
def test_sample_transactions() -> List[Dict]:
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"code": "USD", "name": "USD"}},
            "description": "Tx1 USD"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"code": "EUR", "name": "EUR"}},
            "description": "Tx2 EUR"
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300", "currency": {"code": "USD", "name": "USD"}},
            "description": "Tx3 USD"
        },
    ]


# Параметризованный тест: проверка фильтрации для разных валют
@pytest.mark.parametrize("currency, expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("RUB", []),  # несуществующая валюта
])
def test_filter_by_currency(sample_transactions, currency, expected_ids):
    gen = filter_by_currency(sample_transactions, currency)
    result = list(gen)
    assert [txn["id"] for txn in result] == expected_ids


# Тест с пустым списком транзакций
def test_filter_by_currency_empty_list():
    gen = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(gen)


# Тест когда нет совпадений по валюте, но ген пуст не вызывает ошибку сразу при создании
def test_filter_by_currency_no_matching(sample_transactions):
    gen = filter_by_currency(sample_transactions, "JPY")
    # при первом next — StopIteration

    with pytest.raises(StopIteration):
        next(gen)


# Тест: итератор не завершается до exhausting
def test_filter_by_currency_iterator_exhausts_exactly():
    gen = filter_by_currency(sample_transactions, "USD")

    # мы ожидаем два элемента
    assert next(gen)["id"] == 1
    assert next(gen)["id"] == 3
    with pytest.raises(StopIteration):
        next(gen)


@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
    ]


# Пустой список
@pytest.fixture
def empty_transactions() -> List[Dict]:
    return []


# Тест для transaction_descriptions
@pytest.mark.parametrize(
    "txns, expected",
    [
        pytest.param(
            [{"description": "A"}, {"description": "B"}, {"description": "C"}],
            ["A", "B", "C"],
            id="simple-3"),
        pytest.param(
            [{"description": "X"}],
            ["X"],
            id="single"),
        pytest.param([], [], id="empty"),
    ],
)
def test_transaction_descriptions(txns, expected):
    gen = transaction_descriptions(txns)
    result = list(gen)
    assert result == expected


def test_transaction_descriptions_stopiteration(empty_transactions):
    gen = transaction_descriptions(empty_transactions)
    with pytest.raises(StopIteration):
        next(gen)


# --- Тесты для card_number_generator ---

@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]),
        (9999999999999998, 9999999999999999, [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]),
    ],
)
def test_card_number_generator_range(start, end, expected):
    gen = card_number_generator(start, end)
    result = list(gen)
    assert result == expected


def test_card_number_generator_format():
    # Проверяем формат каждой строки: четыре группы по 4 символа, все цифры
    gen = card_number_generator(1234, 1236)
    items = list(gen)
    for s in items:
        parts = s.split(" ")
        assert len(parts) == 4
        assert all(len(p) == 4 and p.isdigit() for p in parts)


def test_card_number_generator_exhaustion():
    gen = card_number_generator(2, 2)
    first = next(gen)
    assert first == "0000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(gen)
