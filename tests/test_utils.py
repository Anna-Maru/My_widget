import json
import os

import pytest

from src.utils import get_data


class TestGetData:

    def test_get_data_valid_file(self, tmp_path):
        """Тест чтения корректного JSON-файла с данными"""
        test_data = [
            {
                "id": 123,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "amount": {"amount": "1000.00", "currency": {"code": "RUB"}}
            },
            {
                "id": 456,
                "state": "CANCELED",
                "date": "2019-07-03T18:35:29.512364",
                "amount": {"amount": "500.00", "currency": {"code": "USD"}}
            }
        ]

        json_file = tmp_path / "test_operations.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        result = get_data(str(json_file))

        assert result == test_data
        assert len(result) == 2
        assert result[0]["id"] == 123
        assert result[1]["state"] == "CANCELED"

    def test_get_data_nonexistent_file(self):
        """Тест с несуществующим файлом"""
        result = get_data("nonexistent_file.json")
        assert result == []

    def test_get_data_empty_file(self, tmp_path):
        """Тест с пустым файлом"""
        empty_file = tmp_path / "empty.json"
        empty_file.touch()

        result = get_data(str(empty_file))
        assert result == []

    def test_get_data_invalid_json(self, tmp_path):
        """Тест с некорректным JSON"""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write('{"invalid": json}')

        result = get_data(str(invalid_file))
        assert result == []

    def test_get_data_not_a_list(self, tmp_path):
        """Тест когда JSON содержит не список, а объект"""
        not_list_file = tmp_path / "not_list.json"
        with open(not_list_file, 'w') as f:
            json.dump({"key": "value"}, f)

        result = get_data(str(not_list_file))
        assert result == []

    def test_get_data_list_with_non_dict_items(self, tmp_path):
        """Тест когда список содержит не только словари"""
        mixed_file = tmp_path / "mixed.json"
        mixed_data = [
            {"id": 1, "name": "valid"},
            "not a dict",
            123,
            {"id": 2, "name": "also valid"}
        ]
        with open(mixed_file, 'w') as f:
            json.dump(mixed_data, f)

        result = get_data(str(mixed_file))
        assert result == []

    def test_get_data_empty_list(self, tmp_path):
        """Тест с пустым списком в JSON"""
        empty_list_file = tmp_path / "empty_list.json"
        with open(empty_list_file, 'w') as f:
            json.dump([], f)

        result = get_data(str(empty_list_file))
        assert result == []

    def test_get_data_valid_empty_dicts(self, tmp_path):
        """Тест со списком пустых словарей"""
        empty_dicts_file = tmp_path / "empty_dicts.json"
        test_data = [{}, {}, {}]
        with open(empty_dicts_file, 'w') as f:
            json.dump(test_data, f)

        result = get_data(str(empty_dicts_file))
        assert result == test_data
        assert len(result) == 3

    def test_get_data_unicode_content(self, tmp_path):
        """Тест с содержимым на кириллице"""
        unicode_file = tmp_path / "unicode.json"
        test_data = [
            {
                "description": "Перевод организации",
                "from": "Карта 1234",
                "to": "Счёт 5678",
                "currency": "руб."
            }
        ]
        with open(unicode_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        result = get_data(str(unicode_file))
        assert result == test_data
        assert result[0]["description"] == "Перевод организации"

    def test_get_data_file_permission_error(self, tmp_path):
        """Тест с файлом без прав на чтение (только для Unix-систем)"""
        if os.name != 'posix':
            pytest.skip("Test only for Unix-like systems")

        restricted_file = tmp_path / "restricted.json"
        with open(restricted_file, 'w') as f:
            json.dump([{"test": "data"}], f)

        os.chmod(restricted_file, 0o000)
        try:
            result = get_data(str(restricted_file))
            assert result == []
        finally:
            os.chmod(restricted_file, 0o644)
