import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Ищет транзакции по слову или фразе в описании с использованием регулярных выражений"""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [txn for txn in data if pattern.search(txn.get("description", ""))]


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям (по полю description)"""
    desc_counter = Counter(txn.get("description", "").lower() for txn in data)

    result: Dict[str, int] = {}
    for cat in categories:
        cat_lower = cat.lower()
        result[cat] = sum(cnt for desc, cnt in desc_counter.items() if cat_lower in desc)

    return result
