import json
from pathlib import Path

from src.lab05.json_csv import check_suffix
from src.lab08.models import student_to_dict, student_from_dict
from src.lab04.io_txt_csv import read_text


def students_to_json(students, path):
    """Сериализует список студентов и сохраняет его в JSON-файл.

    Принимает список записей о студентах и путь к файлу.
    Проверяет расширение файла, при необходимости создаёт родительские директории.
    Преобразует записи студентов в словари и записывает их в JSON.
    Использует UTF-8, сохраняет кириллицу и форматирует JSON с отступами.
    """
    check_suffix(path, ".json")

    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)

    data = [student_to_dict(student) for student in students]

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path) -> list[dict]:
    """Десериализует JSON-файл и возвращает список записей о студентах.

    Принимает путь к JSON-файлу.
    Проверяет расширение и наличие содержимого в файле.
    Преобразует JSON в Python-объекты, проверяет структуру списка
    и валидирует каждую запись с помощью student_from_dict.
    При ошибках десериализации или некорректной записи вызывает ValueError.
    Возвращает список проверенных словарей с данными студентов.
    """
    check_suffix(path, ".json")

    students = read_text(path).strip()

    if not students:
        raise ValueError("Получен пустой файл")

    list_of_students = []
    try:
        students_load = json.loads(students)
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка десериализации из файла {path}")

    if not isinstance(students_load, list):
        raise ValueError(f"Содержимое файла должно быть списком. Получено - {type(students_load)}")

    for num, student in enumerate(students_load):
        try:
            get_st = student_from_dict(student)
            list_of_students.append(get_st)
        except ValueError:
            raise ValueError(f"Ошибка в записи номер {num+1}")

    return list_of_students


if __name__ == "__main__":    
    input_file = "data/lab08/students_input.json"
    output_file = "data/lab08/students_output.json"
    bad_file = "data/lab08/students_bad.json"

    print(f"1. Чтение из {input_file} и сохранение в {output_file}:")
    try:
        students_list = students_from_json(input_file)
        print(f"Успешно загружено записей: {len(students_list)}") 
        students_to_json(students_list, output_file)
    except Exception as e:
        print(f"Ошибка: {e}")

    print(f"2. Попытка загрузить файл с ошибками ({bad_file}):")
    try:
        students_from_json(bad_file)
    except ValueError as e:
        print(f"Ошибка: {e}")