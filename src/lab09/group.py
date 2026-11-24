"""
Модуль для хранения и управления данными студентов в CSV-файле.

Содержит функции для создания хранилища, загрузки и сохранения
записей, а также добавления, поиска, удаления и обновления студентов.
"""

import csv
from pathlib import Path
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student


def save_students(path, students):
    """
    Сохраняет список студентов в CSV-файл.

    Перед сохранением проверяет корректность каждой записи.
    Создает CSV-файл с заголовками, соответствующими STUDENT_FIELDS.

    Args:
        path: Путь к CSV-файлу.
        students: Список словарей с данными студентов.
    """
    
    for student in students:
        validate_student(student)
        
    path = Path(path)
    
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        writer.writerows(students)
    
    
def ensure_storage(path):
    """
    Проверяет наличие CSV-хранилища и создает его при необходимости.

    Если файл отсутствует, создает родительские каталоги
    и новый CSV-файл с заголовками.

    Args:
        path: Путь к CSV-файлу хранилища.
    """
    path = Path(path)
    
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    save_students(path, [])
    
    
def load_students(path) -> list[dict]:
    """
    Загружает записи студентов из CSV-файла.

    Проверяет наличие заголовка и соответствие названий колонок
    установленному формату. Преобразует GPA в число и проверяет
    корректность каждой записи.

    Args:
        path: Путь к CSV-файлу хранилища.

    Returns:
        list[dict]: Список словарей с данными студентов.

    Raises:
        ValueError: Если заголовок или данные файла некорректны.
    """
    path = Path(path)
     
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
         
        if reader.fieldnames is None:
            raise ValueError(f"В файле {path} отсутствует заголовок")
         
        columns = set(reader.fieldnames)
         
        if columns != set(STUDENT_FIELDS):
            extra = columns - set(STUDENT_FIELDS)
            missed = set(STUDENT_FIELDS) - columns
            raise ValueError(f"Колонки несоответствуют стандарту в файле {path}. Лишние: {extra}; пропущенные: {missed}")
        
        students = []
        
        for num, student in enumerate(reader):
            
            try:
                try:
                    student["gpa"] = float(student["gpa"])
                except (TypeError, ValueError) as e:
                    raise ValueError(f"Некорректное значение GPA: {student['gpa']!r}") from e
                students.append(student_from_dict(student))
            except ValueError as e:
                raise ValueError(f"Ошибка {e} в записи номер {num + 1}") from e
            
    return students
    
def add_student(path, student):
    """
    Добавляет нового студента в CSV-хранилище.

    Проверяет данные студента, загружает существующие записи,
    добавляет новую запись и сохраняет обновленный список.

    Args:
        path: Путь к CSV-файлу хранилища.
        student: Словарь с данными добавляемого студента.
    """
    ensure_storage(path)
    student = student_from_dict(student)
    students = load_students(path)
    students.append(student)
    save_students(path, students)
    
    
def list_students(path, sort_by=None):
    """
    Возвращает список студентов из CSV-хранилища.

    При необходимости сортирует записи по ФИО или среднему баллу GPA.

    Args:
        path: Путь к CSV-файлу хранилища.
        sort_by: Поле сортировки: "fio", "gpa" или None.

    Returns:
        list[dict]: Список записей студентов.

    Raises:
        ValueError: Если указано неподдерживаемое поле сортировки.
    """
    ensure_storage(path)
    students = load_students(path)
    if sort_by is not None:
        if sort_by not in ("fio", "gpa"):
            raise ValueError("Сортировка доступна только по fio или gpa")
        students.sort(key=lambda student: student[sort_by])
    return students
    
    
def find_students(path, substr):
    """
    Находит студентов по подстроке в ФИО.

    Поиск выполняется без учета регистра символов.

    Args:
        path: Путь к CSV-файлу хранилища.
        substr: Подстрока для поиска в ФИО.

    Returns:
        list[dict]: Список студентов, ФИО которых содержит указанную подстроку.
    """
    ensure_storage(path)
    query = substr.casefold()
    return [student for student in load_students(path) if query in student["fio"].casefold()] 
    
    
def remove_student(path, fio):
    """
    Удаляет из хранилища все записи с указанным ФИО.

    Args:
        path: Путь к CSV-файлу хранилища.
        fio: Полное ФИО студента для удаления.

    Returns:
        int: Количество удаленных записей.
    """
    ensure_storage(path)
    students = load_students(path)
    remaining = [student for student in students if student["fio"] != fio]
    removed = len(students) - len(remaining)
    if removed:
        save_students(path, remaining)
    return removed
    
    
def update_student(path, fio, **fields):
    """
    Обновляет данные первого найденного студента с указанным ФИО.

    Проверяет переданные поля, формирует обновленную запись
    и сохраняет изменения в CSV-файл.

    Args:
        path: Путь к CSV-файлу хранилища.
        fio: ФИО студента, данные которого нужно обновить.
        **fields: Поля и новые значения для обновления.

    Returns:
        bool: True, если студент найден и обновлен, иначе False.

    Raises:
        ValueError: Если поля не указаны, содержат неизвестные
            названия или включают поле fio.
    """
    if not fields:
        raise ValueError("Укажите хотя бы одно поле для обновления")

    unknown = set(fields) - set(STUDENT_FIELDS)
    if unknown:
        raise ValueError(f"Неизвестные поля: {', '.join(sorted(unknown))}")

    if "fio" in fields:
        raise ValueError("Поле fio нельзя обновлять этой командой")

    ensure_storage(path)
    students = load_students(path)

    for index, student in enumerate(students):
        if student["fio"] == fio:
            updated_student = student_from_dict({**student, **fields})

            students[index] = updated_student
            save_students(path, students)

            return True

    return False
