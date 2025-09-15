# Виджет финансовых операций

## Описание:

Удобный виджет для личного кабинета банка, который выводит последние успешные финансовые операции клиента.  
Поддерживает работу с различными источниками данных и дополнительный функционал по обработке транзакций.

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
   Зависимости: black, isort, flake8, mypy, pytest, pytest-cov, pandas, openpyxl, requests, python-dotenv

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
5. Реализован декоратор log
```
def log(filename: str = None):
    """Декоратор для логирования выполнения функций"""
```
Его функции:
* Логирование в файл или консоль
* Форматирование с временными метками
* Обработка исключений
* Сохранение оригинальной функции

Пример использования: 
```
@log("mylog.txt")
def my_function(x, y):
    return x + y`
```
6. Загрузка данных из файлов

Финансовые транзакции теперь можно загружать не только из JSON, но и из CSV и Excel:
```from src.utils import get_data
from src.readers import read_csv, read_excel

# JSON
transactions_json = get_data("data/operations.json")

# CSV
transactions_csv = read_csv("data/transactions.csv")

# Excel
transactions_excel = read_excel("data/transactions_excel.xlsx")
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
6. Покрытие кода
```bash
pytest --cov=app tests/
```
**Результат**: 99% покрытия.