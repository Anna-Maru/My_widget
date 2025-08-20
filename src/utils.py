import json
import os
from typing import List, Dict, Any


def get_data(json_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        if not os.path.exists(json_path):
            return []

        if os.path.getsize(json_path) == 0:
            return []

        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            return []

        if not all(isinstance(item, dict) for item in data):
            return []

        return data

    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return []

    except Exception:
        return []
