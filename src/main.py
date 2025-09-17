import logging
import os
import sys

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.readers import read_csv_transactions, read_excel_transactions
from src.search import process_bank_search
from src.utils import get_data

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/main.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main():
    logger.info("Программа запущена")

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    if choice == "1":
        path = "data/operations.json"
        data = get_data(path)
        print("Для обработки выбран JSON-файл.")
        logger.info("Загружены данные из JSON: %s", path)
    elif choice == "2":
        path = "data/transactions.csv"
        data = read_csv_transactions(path)
        print("Для обработки выбран CSV-файл.")
        logger.info("Загружены данные из CSV: %s", path)
    elif choice == "3":
        path = "data/transactions_excel.xlsx"
        data = read_excel_transactions(path)
        print("Для обработки выбран XLSX-файл.")
        logger.info("Загружены данные из Excel: %s", path)
    else:
        print("Неверный выбор.")
        logger.error("Пользователь сделал неверный выбор: %s", choice)
        sys.exit(1)

    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(f"Введите статус для фильтрации ({', '.join(statuses)}): ").upper()
        if status in statuses:
            data = filter_by_state(data, state=status)
            print(f"Операции отфильтрованы по статусу {status}")
            logger.info("Фильтрация по статусу: %s", status)
            break
        else:
            print(f"Статус операции '{status}' недоступен.")
            logger.warning("Некорректный статус: %s", status)

    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").lower()
    if sort_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        data = sort_by_date(data, ascending=(order == "по возрастанию"))
        logger.info("Данные отсортированы по дате (%s)", order)

    rub_choice = input("Выводить только рублевые транзакции? Да/Нет: ").lower()
    if rub_choice == "да":
        data = list(filter_by_currency(data, "RUB"))
        logger.info("Отфильтрованы только рублевые транзакции")

    search_choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower()
    if search_choice == "да":
        word = input("Введите слово для поиска: ")
        data = process_bank_search(data, word)
        logger.info("Фильтрация по слову в описании: %s", word)

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        logger.warning("Выборка пустая")
    else:
        print("Распечатываю итоговый список транзакций...")
        print(f"\nВсего банковских операций в выборке: {len(data)}\n")
        logger.info("Итоговый список: %d операций", len(data))

        for txn in data:
            print(f"{txn.get('date', '')} {txn.get('description', '')}")
            print(f"{txn.get('from', '')} -> {txn.get('to', '')}")
            print(f"Сумма: {txn.get('operationAmount', {}).get('amount', '')} "
                  f"{txn.get('operationAmount', {}).get('currency', {}).get('name', '')}\n")

    logger.info("Программа завершена")


if __name__ == "__main__":
    main()
