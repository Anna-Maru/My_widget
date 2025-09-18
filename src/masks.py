import logging
from pathlib import Path
from typing import Union


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "masks.log"


LOG_DIR.mkdir(parents=True, exist_ok=True)

if not LOG_FILE.exists():
    LOG_FILE.touch()


logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number: Union[int, str]) -> str:
    """ Функция маскирует номер банковской карты в формате XXXX XX** **** XXXX.
        Формат маскировки:
          - первые 6 цифр отображаются полностью:
            отдельные блоки — первые 4 цифры (XXXX),
            затем следующие 2 цифры плюс две звездочки (XX**),
          - далее — четыре звездочки (****),
          - и последние 4 цифры видимы (XXXX).
        Args:
            number (int | str): Номер карты, возможно с пробелами.
        Return:
            str: Строка с замаскированным номером.
                 Если длина строки менее 10 символов после очистки,
                 возвращается строка без изменений."""
    try:
        s = str(number).replace(" ", "")
        if len(s) < 10:
            logger.error("Ошибка маскировки карты: номер слишком короткий (%s)", s)
            return s

        part1 = s[:4]
        part2 = s[4:6] + "**"
        part3 = "****"
        part4 = s[-4:]

        masked = f"{part1} {part2} {part3} {part4}"
        logger.info("Успешно замаскирован номер карты")
        return masked

    except Exception as ex:
        logger.error("Ошибка маскировки номера карты: %s", ex)
        raise


def get_mask_account(number: Union[int, str]) -> str:
    """ Функция маскирует номер банковского счёта в формате **XXXX.
        Формат маскировки:
          - две звёздочки в начале,
          - далее — последние 4 цифры счёта.
        Args:
            number (int | str): Номер счёта, возможно с пробелами.
        Return:
            str: Строка с замаскированным счётом.
                 Если длина строки ≤4 после очистки, возвращается без изменений."""
    try:
        s = str(number).replace(" ", "")
        if len(s) <= 4:
            logger.error("Короткий номер счёта: %s", s)
            return s

        masked = f"**{s[-4:]}"
        logger.info("Успешно замаскирован номер счёта")
        return masked

    except Exception as ex:
        logger.error("Ошибка маскировки номера счёта: %s", ex)
        raise
