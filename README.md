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
4. Генераторы для операций и номеров карт (`filter_by_currency`, `card_number_generator`)
```
transactions = [...]
for txn in filter_by_currency(transactions, "USD"):
    print(txn)
   ```

### Тесты
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустить все тесты:
   ```bash
   pytest tests/ -v
   ```
3. Для конкретного файла:
   ```bash
   pytest tests/test_masks.py -v
   ```
   ```bash
   pytest tests/test_widget.py -v
   ```
   ```bash
   pytest tests/test_processing.py -v
   ```
   ```bash
   pytest tests/test_generators.py -v
   ```
5. Покрытие кода
```bash
pytest --cov=app tests/
```
**Результат**: 99% покрытия.