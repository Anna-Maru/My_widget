import pandas as pd
from typing import List, Dict, Any


def read_csv_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из CSV-файла."""
    try:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []
    except Exception:
        return []


def read_excel_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из Excel-файла (.xlsx)."""
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except (FileNotFoundError, ValueError):
        return []
    except Exception:
        return []
