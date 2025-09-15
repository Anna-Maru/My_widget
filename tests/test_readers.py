from unittest.mock import patch, MagicMock
from src import readers


@patch("src.readers.pd.read_csv")
def test_read_csv_transactions_success(mock_read_csv):
    """Тест: корректное чтение CSV-файла."""
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "RUB"},
    ]
    mock_read_csv.return_value = mock_df

    result = readers.read_csv_transactions("fake_path.csv")

    assert isinstance(result, list)
    assert result[0]["currency"] == "USD"
    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.readers.pd.read_csv", side_effect=FileNotFoundError)
def test_read_csv_transactions_file_not_found(mock_read_csv):
    """Тест: возвращается пустой список, если CSV-файл не найден."""
    result = readers.read_csv_transactions("no_file.csv")
    assert result == []


@patch("src.readers.pd.read_excel")
def test_read_excel_transactions_success(mock_read_excel):
    """Тест: корректное чтение Excel-файла."""
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"id": 10, "amount": 300, "currency": "EUR"},
        {"id": 11, "amount": 400, "currency": "RUB"},
    ]
    mock_read_excel.return_value = mock_df

    result = readers.read_excel_transactions("fake_file.xlsx")

    assert isinstance(result, list)
    assert result[1]["amount"] == 400
    mock_read_excel.assert_called_once_with("fake_file.xlsx")


@patch("src.readers.pd.read_excel", side_effect=ValueError("Bad format"))
def test_read_excel_transactions_bad_file(mock_read_excel):
    """Тест: возвращается пустой список при ошибке чтения Excel."""
    result = readers.read_excel_transactions("bad_file.xlsx")
    assert result == []
