from typing import Dict, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"amount": "100", "currency": {"code": "USD", "name": "USD"}},
        },
        {
            "id": 2,
            "description": "Перевод со счета на счет",
            "operationAmount": {"amount": "200", "currency": {"code": "EUR", "name": "EUR"}},
        },
        {
            "id": 3,
            "description": "Перевод с карты на карту",
            "operationAmount": {"amount": "300", "currency": {"code": "USD", "name": "USD"}},
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Dict]:
    return []


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("RUB", []),
    ]
)
def test_filter_by_currency(sample_transactions, currency, expected_ids):
    gen = filter_by_currency(sample_transactions, currency)
    result = list(gen)
    assert [txn["id"] for txn in result] == expected_ids


def test_filter_by_currency_empty_list():
    gen = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_no_matching(sample_transactions):
    gen = filter_by_currency(sample_transactions, "JPY")
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_iterator_exhausts_exactly(sample_transactions):
    gen = filter_by_currency(sample_transactions, "USD")
    assert next(gen)["id"] == 1
    assert next(gen)["id"] == 3
    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "txns, expected",
    [
        ([{"description": "A"}, {"description": "B"}, {"description": "C"}], ["A", "B", "C"]),
        ([{"description": "X"}], ["X"]),
        ([], []),
    ]
)
def test_transaction_descriptions(txns, expected):
    gen = transaction_descriptions(txns)
    result = list(gen)
    assert result == expected


def test_transaction_descriptions_stopiteration_empty(empty_transactions):
    gen = transaction_descriptions(empty_transactions)
    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ]
)
def test_card_number_generator_range(start, end, expected):
    gen = card_number_generator(start, end)
    result = list(gen)
    assert result == expected


def test_card_number_generator_format():
    gen = card_number_generator(1234, 1236)
    for s in list(gen):
        parts = s.split(" ")
        assert len(parts) == 4
        assert all(len(p) == 4 and p.isdigit() for p in parts)


def test_card_number_generator_exhaustion():
    gen = card_number_generator(2, 2)
    assert next(gen) == "0000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(gen)
