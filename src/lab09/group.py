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
                students.append(student_from_dict(student))
            except ValueError as e:
                raise ValueError(f"Ошибка {e} в записи номер {num+1}")
            
    return students
    
    
    
