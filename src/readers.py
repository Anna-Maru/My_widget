import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/readers.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def read_csv_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из CSV-файла."""
    try:
        df = pd.read_csv(path)
        logger.debug(f"CSV-файл {path} успешно загружен. Количество строк: {len(df)}")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"CSV-файл {path} не найден.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"CSV-файл {path} пустой.")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {path}: {e}")
        return []


def read_excel_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из Excel-файла (.xlsx)."""
    try:
        df = pd.read_excel(path)
        logger.debug(f"Excel-файл {path} успешно загружен. Количество строк: {len(df)}")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Excel-файл {path} не найден.")
        return []
    except ValueError as e:
        logger.error(f"Ошибка при чтении Excel-файла {path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel-файла {path}: {e}")
        return []
