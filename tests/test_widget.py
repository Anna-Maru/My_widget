from my_widget.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счёт 0000111122223333", "Счёт 0000 11** **** 3333"),
    ],
)
def test_mask_account_card(info, expected):
    assert mask_account_card(info) == expected


def test_mask_account_card_empty_or_invalid():
    assert mask_account_card("") == ""
    # Без пробела — весь текст считается номером → маскируем как карту
    assert mask_account_card("1234567890123456") == "1234 56** **** 3456"


@pytest.mark.parametrize(
    "iso, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2000-12-01T00:00:00", "01.12.2000"),
    ],
)
def test_get_date_valid(iso, expected):
    assert get_date(iso) == expected


def test_get_date_invalid():
    invalid = "not-a-date"
    assert get_date(invalid) == invalid