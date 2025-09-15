from typing import Any, Dict, List


def filter_by_state(
    records: List[Dict[str, Any]],
    state: str = "EXECUTED",
) -> List[Dict[str, Any]]:
    """Отфильтровывает список записей по значению ключа "state".

    Args:
        records (list of dict): Список словарей, каждый содержит ключ "state".
        state (str, optional): Статус для фильтрации. По умолчанию "EXECUTED".

    Returns:
        list of dict: Новый список, содержащий только те словари,
        где значение records[i]['state'] == state.
    """
    return [rec for rec in records if rec.get("state") == state]


def sort_by_date(
    records: List[Dict[str, Any]],
    descending: bool = True,
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу "date'.

    Args:
        records (List[Dict[str, Any]]): Список операций, каждая с ключом "date" в ISO-формате.
        descending (bool, optional): Если True (по умолчанию) — сортирует по убыванию,
                                     иначе — по возрастанию.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список записей.
    """
    return sorted(records, key=lambda x: x.get("date", ""), reverse=descending)
