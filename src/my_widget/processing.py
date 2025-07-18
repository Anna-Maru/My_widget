from typing import Any, Dict, List

def filter_by_state(
    records: List[Dict[str, Any]],
    state: str = "EXECUTED",
) -> List[Dict[str, Any]]:
    """Отфильтровывает список записей по значению ключа "state"."""
    return [rec for rec in records if rec.get("state") == state]


def sort_by_date(
    records: List[Dict[str, Any]],
    descending: bool = True,
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу "date'.
    """
    return sorted(records, key=lambda x: x.get("date", ""), reverse=descending)