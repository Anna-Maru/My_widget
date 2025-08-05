import pytest

from src.decorators import log


class TestLogDecorator:

    def test_successful_function_console_output(self, capsys):
        """Тест успешного выполнения функции с выводом в консоль"""

        @log()
        def add_numbers(x, y):
            return x + y

        result = add_numbers(1, 2)

        assert result == 3

        captured = capsys.readouterr()
        assert captured.out.strip() == "add_numbers ok"

    def test_successful_function_file_output(self, tmp_path):
        """Тест успешного выполнения функции с записью в файл"""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def multiply(a, b):
            return a * b

        result = multiply(3, 4)

        assert result == 12

        assert log_file.exists()
        content = log_file.read_text(encoding='utf-8')
        assert content.strip() == "multiply ok"

    def test_function_error_console_output(self, capsys):
        """Тест функции с ошибкой и выводом в консоль"""
        @log()
        def divide_by_zero(x):
            return x / 0

        with pytest.raises(ZeroDivisionError):
            divide_by_zero(10)

        captured = capsys.readouterr()
        expected = "divide_by_zero error: ZeroDivisionError. Inputs: (10,), {}"
        assert captured.out.strip() == expected

    def test_function_error_file_output(self, tmp_path):
        """Тест функции с ошибкой и записью в файл"""
        log_file = tmp_path / "error_log.txt"

        @log(filename=str(log_file))
        def invalid_conversion():
            return int("abc")

        with pytest.raises(ValueError):
            invalid_conversion()

        assert log_file.exists()
        content = log_file.read_text(encoding='utf-8')
        expected = "invalid_conversion error: ValueError. Inputs: (), {}"
        assert content.strip() == expected

    def test_function_with_args_and_kwargs(self, capsys):
        """Тест функции с позиционными и именованными аргументами"""
        @log()
        def complex_function(a, b, c=None, d=42):
            if c is None:
                raise TypeError("c cannot be None")
            return a + b + c + d

        with pytest.raises(TypeError):
            complex_function(1, 2, d=100)

        captured = capsys.readouterr()
        expected = "complex_function error: TypeError. Inputs: (1, 2), {'d': 100}"
        assert captured.out.strip() == expected

    def test_multiple_calls_to_file(self, tmp_path):
        """Тест множественных вызовов с записью в один файл"""
        log_file = tmp_path / "multiple_calls.txt"

        @log(filename=str(log_file))
        def simple_func(x):
            return x * 2

        simple_func(1)
        simple_func(2)
        simple_func(3)

        content = log_file.read_text(encoding='utf-8')
        lines = content.strip().split('\n')
        assert len(lines) == 3
        assert all(line == "simple_func ok" for line in lines)

    def test_decorator_preserves_function_metadata(self):
        """Тест, что декоратор сохраняет метаданные функции"""
        @log()
        def documented_function(x, y):
            """This function adds two numbers."""
            return x + y

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This function adds two numbers."

    def test_no_filename_parameter(self, capsys):
        """Тест декоратора без параметра filename"""

        @log()
        def no_param_func():
            return "success"
        result = no_param_func()
        assert result == "success"

        captured = capsys.readouterr()
        assert captured.out.strip() == "no_param_func ok"
