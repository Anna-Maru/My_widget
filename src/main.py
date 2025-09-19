import sys

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.readers import read_csv_transactions, read_excel_transactions
from src.search import process_bank_search
from src.utils import get_data


def main():
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
    elif choice == "2":
        path = "data/transactions.csv"
        data = read_csv_transactions(path)
        print("Для обработки выбран CSV-файл.")
    elif choice == "3":
        path = "data/transactions_excel.xlsx"
        data = read_excel_transactions(path)
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор.")
        sys.exit(1)

    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(f"Введите статус для фильтрации ({', '.join(statuses)}): ").upper()
        if status in statuses:
            data = filter_by_state(data, state=status)
            print(f"Операции отфильтрованы по статусу {status}")
            break
        else:
            print(f"Статус операции '{status}' недоступен.")

    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").lower()
    if sort_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        data = sort_by_date(data, descending=(order == "по убыванию"))

    rub_choice = input("Выводить только рублевые транзакции? Да/Нет: ").lower()
    if rub_choice == "да":
        data = list(filter_by_currency(data, "RUB"))

    search_choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower()
    if search_choice == "да":
        word = input("Введите слово для поиска: ")
        data = process_bank_search(data, word)

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print("Распечатываю итоговый список транзакций...")
        print(f"\nВсего банковских операций в выборке: {len(data)}\n")
        for txn in data:
            print(f"{txn.get('date', '')} {txn.get('description', '')}")
            print(f"{txn.get('from', '')} -> {txn.get('to', '')}")
            print(f"Сумма: {txn.get('operationAmount', {}).get('amount', '')} "
                  f"{txn.get('operationAmount', {}).get('currency', {}).get('name', '')}\n")


if __name__ == "__main__":
    main()
