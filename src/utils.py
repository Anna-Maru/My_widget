import json
import logging
import os
from typing import Any, Dict, List


logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data(json_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        if not os.path.exists(json_path):
            logger.error("Файл не найден: %s", json_path)
            return []

        if os.path.getsize(json_path) == 0:
            logger.error("Файл пустой: %s", json_path)
            return []

        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            logger.error("Содержимое файла %s не является списком", json_path)
            return []

        if not all(isinstance(item, dict) for item in data):
            logger.error("Содержимое файла %s содержит не словари", json_path)
            return []

        logger.info("Успешно загружено %d транзакций из %s", len(data), json_path)
        return data

    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as ex:
        logger.error("Ошибка чтения JSON из %s: %s", json_path, ex)
        return []

    except OSError as ex:
        logger.error("Ошибка доступа к файлу %s: %s", json_path, ex)
        return []

    except Exception as ex:
        logger.error("Неожиданная ошибка при обработке %s: %s", json_path, ex)
        return []
