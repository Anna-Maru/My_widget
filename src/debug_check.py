import os
from src.utils import get_data

print("=== ОТЛАДКА ===")
print("Текущая директория:", os.getcwd())
print("Существует ли файл:", os.path.exists("data/operations.json"))

if os.path.exists("data/operations.json"):
    print("Размер файла:", os.path.getsize("data/operations.json"), "байт")

current_dir = os.getcwd()
json_path = os.path.join(current_dir, "data", "operations.json")
print("Полный путь:", json_path)

data = get_data("data/operations.json")
print("Загружено операций:", len(data))

