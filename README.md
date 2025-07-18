# Виджет финансовых операций

## Описание:

Удобный виджет для личного кабинета банка, который выводит последние успешные финоперации клиента.

### Установка

1. Клонируйте репозиторий
```
git clone https://github.com/Anna-Maru/My_widget
```

2. Создайте виртуальное окружение

poetry install --with lint,test

3. Убедитесь, что установлены:
   python 3.15
   Poetry
   Зависимости: black, isort, flake8, mypy, pytest

### Использование

1. Маскировка карт и счетов
   ```from widget.py import mask_account_card
   print(mask_account_card("Visa Platinum 7000792289606361"))

   print(mask_account_card("Счет 73654108430135874305"))
2. Преобразование даты
   ```from widget.py import get_date
   print(get_date("2024-03-11T02:26:18.671407"))
   ```
3. Фильтрация и сортировка операций
```from processing.py import filter_by_state, sort_by_date

records = [
    {"id": 1, "state": "EXECUTED", "date": "..."},
    {"id": 2, "state": "CANCELED", "date": "..."},
]

executed = filter_by_state(records)
sorted_ops = sort_by_date(executed)
```