import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "перевод с карты на карту"},
        {"id": 5, "description": "Списание комиссии"},
    ]


@pytest.mark.parametrize(
    "search, expected_ids",
    [
        ("перевод", [1, 2, 4]),
        ("Открытие", [3]),
        ("комиссии", [5]),
        ("несуществующая", []),
    ],
)
def test_process_bank_search(sample_transactions, search, expected_ids):
    result = process_bank_search(sample_transactions, search)
    ids = [txn["id"] for txn in result]
    assert ids == expected_ids


def test_process_bank_search_case_insensitive(sample_transactions):
    result_lower = process_bank_search(sample_transactions, "перевод")
    result_upper = process_bank_search(sample_transactions, "ПЕРЕВОД")
    assert result_lower == result_upper


def test_process_bank_search_empty_list():
    assert process_bank_search([], "перевод") == []


@pytest.mark.parametrize(
    "categories, expected",
    [
        (
            ["Перевод", "Открытие вклада"],
            {"Перевод": 3, "Открытие вклада": 1},
        ),
        (
            ["Списание комиссии", "Неизвестная"],
            {"Списание комиссии": 1, "Неизвестная": 0},
        ),
    ],
)
def test_process_bank_operations(sample_transactions, categories, expected):
    result = process_bank_operations(sample_transactions, categories)
    assert result == expected


def test_process_bank_operations_empty_data():
    categories = ["Перевод", "Открытие вклада"]
    result = process_bank_operations([], categories)
    assert result == {"Перевод": 0, "Открытие вклада": 0}
