import csv
from pathlib import Path
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student


def save_students(path, students):
    
    for student in students:
        validate_student(student)
        
    path = Path(path)
    
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        writer.writerows(students)
    
    
def ensure_storage(path):
    path = Path(path)
    
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    save_students(path, [])
    
    
def load_students(path) -> list[dict]:
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
    ensure_storage(path)
    student = student_from_dict(student)
    students = load_students(path)
    students.append(student)
    save_students(path, students)
    
    
def list_students(path, sort_by=None):
    ensure_storage(path)
    students = load_students(path)
    if sort_by is not None:
        if sort_by not in ("fio", "gpa"):
            raise ValueError("Сортировка доступна только по fio или gpa")
        students.sort(key=lambda student: student[sort_by])
    return students
    
    
def find_students(path, substr):
    ensure_storage(path)
    query = substr.casefold()
    return [student for student in load_students(path) if query in student["fio"].casefold()] 
    
    
def remove_student(path, fio):
    ensure_storage(path)
    students = load_students(path)
    remaining = [student for student in students if student["fio"] != fio]
    removed = len(students) - len(remaining)
    if removed:
        save_students(path, remaining)
    return removed
    
    
def update_student(path, fio, **fields):
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

    
    
    
