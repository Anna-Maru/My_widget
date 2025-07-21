import pytest
from masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        (7000792289606361, "7000 79** **** 6361"),
        ("1234567890", "1234 56** **** 7890"),
        ("123456789", "123456789"),
    ]
)
def test_get_mask_card_number(number, expected):
    assert get_mask_card_number(number) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        ("73654108430135874305", "**4305"),
        (73654108430135874305, "**4305"),
        ("1234", "1234"),
        ("123", "123"),
    ]
)
def test_get_mask_account(number, expected):
    assert get_mask_account(number) == expected