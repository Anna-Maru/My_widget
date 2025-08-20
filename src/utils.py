import json
from pathlib import Path
from typing import Any, List, Dict


def load_transactions_from_json(path: str | Path) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла.
        Если файл отсутствует, не читается корректно, или JSON не является списком,
        возвращает пустой список.
        """
    try:
        path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if isinstance(data, list):
        return data
    return []
