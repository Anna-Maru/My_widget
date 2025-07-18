from datetime import datetime
from masks import get_mask_card_number, get_mask_account

def mask_account_card(info: str) -> str:
    """ Маскирует номер банковской карты или счёта из строки, содержащей тип и номер.
    Примеры:
      "Visa Platinum 7000792289606361" →
        "Visa Platinum 7000 79** **** 6361"
      "Счет 73654108430135874305" →
        "Счет **4305"
    Функция парсит входную строку, разделяя
    на предшествующий текст и номер,
    затем применяет соответствующую маскировку:
      - карты — через get_mask_card_number,
      - счета — через get_mask_account.

    Args:
        info (str): Одна строка, где в конце — номер карты или счёта.

    Return:
        str: Исходная строка с замаскированным номером."""
    parts = info.strip().split()
    if not parts:
        return info  # пустая строка

    number = parts[-1]
    prefix = " ".join(parts[:-1])

    # Выбор маскировки
    # Если слово "Счет" или "Счёт" (русская 'ё'), применяем get_mask_account
    low_pref = prefix.lower()
    if low_pref.endswith("счет") or low_pref.endswith("счёт"):
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    return f"{prefix} {masked}"


def get_date(iso_str: str) -> str:
    """ Преобразует ISO-дату и время в формат "ДД.MM.ГГГГ".
    Принимает строку вида "2024-03-11T02:26:18.671407",
    возвращает "11.03.2024".

    Args:
        iso_str (str): Дата и время в ISO-формате.

    Return:
        str: Только дата в формате "ДД.MM.ГГГГ",
             или исходная строка, если парсинг неудачный. """
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return iso_str