import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None):
    """
    Декоратор для автоматического логирования выполнения функций.

    Args:
        filename (str, optional): Имя файла для записи логов.
                                 Если None, логи выводятся в консоль.

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)

                log_message = f"{func.__name__} ok"

                _write_log(log_message, filename)

                return result

            except Exception as e:
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"

                _write_log(log_message, filename)

                raise

        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
        Вспомогательная функция для записи логов в файл или консоль.

        Args:
            message (str): Сообщение для логирования
            filename (str, optional): Имя файла. Если None, выводит в консоль.
        """
    if filename:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(message + '\n')
    else:
        print(message)
