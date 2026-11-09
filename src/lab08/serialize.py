import json
from pathlib import Path

from src.lab05.json_csv import check_suffix
from src.lab08.models import student_to_dict, student_from_dict
from src.lab04.io_txt_csv import read_text


def students_to_json(students, path):
    check_suffix(path, ".json")
    
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    
    data = [student_to_dict(student) for student in students]
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    
def students_from_json(path) -> list[dict]:
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
    
    
    
        
    
    