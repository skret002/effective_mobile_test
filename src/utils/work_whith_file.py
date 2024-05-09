import json
import os
from dataclasses import asdict

from dotenv import load_dotenv

load_dotenv()

file_name=os.getenv("JSON_FILE_NAME")
file_path = os.path.dirname(os.path.dirname(__file__)) + f"/{file_name}"

def read_json_file(file_path: str = file_path):
    """
    Читает данные из JSON файла и возвращает их.

    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {file_path}")

def get_new_id(file_path: str = file_path):
    if os.path.isfile(file_path):
        json_data = read_json_file()
        last_id = json_data[-1]["id"] if len(json_data) > 0 else 0
    else:
        last_id = 0
    print("Отдан id", last_id + 1)
    return last_id + 1
def write_json_file(data: object, file_path: str = file_path):
    """
    Записывает или обновляет данные в JSON файле.
    Сверка данных происходит по ID.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        else:
            json_data = []

        # Проверяем наличие объекта с таким же ID в файле
        updated = False
        for i, item in enumerate(json_data):
            if item['id'] == asdict(data)['id']:
                json_data[i] = asdict(data)  # Обновляем данные
                updated = True
                break

        if not updated:
            json_data.append(asdict(data))  # Добавляем новый объект, если не было обновления

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)

    except IOError:
        print(f"Не удалось записать данные в файл: {file_path}")

def delete_json_post(entry_id: int = None, file_path: str = file_path):
    """
    Удаляет запись по ID из JSON файла. Если ID не указан, удаляет все записи.
    :param entry_id: ID записи для удаления. Если None, удаляются все записи.
    """

    if not os.path.exists(file_path):
        return 'Нечего очищать'
    json_data = read_json_file() #вычитываем
    if entry_id is not None:
        json_data = [item for item in json_data if item.get("id") != entry_id] #сортируем
    else:
        json_data = []
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    return "Данные успешно удалены"
