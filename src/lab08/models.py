from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")

def make_student(fio, birthdate, group, gpa):
    # Валидация GPA
    if isinstance(gpa, (int, float)) and not isinstance(gpa, bool):
        gpa = float(gpa)
        if gpa < 0 or gpa > 5:
            raise ValueError(f"Значение GPA должно быть в диапазоне от 0.0 до 5.0, получено - {gpa}")
    else:
        raise ValueError(f"GPA должно быть в формате int | float, получено в {type(gpa)}")
    #Валидация группы
    if isinstance(group, str):
        group = group.strip()
        if not group:
            raise ValueError("Поле GROUP пустое")
    else:
        raise ValueError(f"GROUP должно быть в формате str, получено в {type(group)}")
    #Валидация даты
    if not isinstance(birthdate, str):
        raise ValueError("Дата должна быть введена в текстовом формате 'YYYY-MM-DD'")
    birthdate = birthdate.strip()
    try:
        date_date = date.fromisoformat(birthdate)
    except ValueError: 
        raise ValueError("Введена неверная дата. Дата ожидается в формате 'YYYY-MM-DD'")
    
    if date_date > date.today():
        raise ValueError("Дата рождения не может быть в будущем")
    #Валидация ФИО
    if isinstance(fio, str):
        fio = fio.strip()
        if not fio:
            raise ValueError("Поле FIO пустое")
    else:
        raise ValueError(f"FIO должно быть в формате str, получено в {type(fio)}")
    
    if len(fio.split()) < 2:
        raise ValueError("В ФИО должна быть хотя бы фамилия и имя")
    
    return {"fio": fio, "birthdate": birthdate, "group": group, "gpa": round(gpa, 2)}

def validate_student(rec):
    #Проверка набора ключей
    if not isinstance(rec, dict):
        raise ValueError(f"Запись должна быть словарем, получено - {type(rec)}")
    get = set(rec.keys())
    need = set(STUDENT_FIELDS)
    if get != need:
        missed = need - get
        extra = get - need
        raise ValueError(f"Ошибка формата записи. Пропущены поля: {missed}. Лишние поля: {extra}")
    #Проверка каждого значения
    make_student(rec["fio"], rec["birthdate"], rec["group"], rec["gpa"])
    
def student_age(rec, today=None):
    today = today or date.today()
    birthday = date.fromisoformat(rec["birthdate"])
    if birthday > today:
        raise ValueError("Дата рождения не может быть в будущем")
    minus_year = 0
    if today.month <= birthday.month and today.day < birthday.day:
        minus_year += 1
    return today.year - birthday.year - minus_year

def student_to_dict(rec):
    validate_student(rec)
    rec_copy = rec.copy()
    return rec_copy

def student_from_dict(d):
    if not isinstance(d, dict):
        raise ValueError(f"Ожидался словарь, получено - {type(d)}")

    fio = d.get("fio")
    birthdate = d.get("birthdate")
    group = d.get("group")
    gpa = d.get("gpa")
    
    if isinstance(gpa, (int, float)) and not isinstance(gpa, bool):
        gpa = float(gpa)

    des_from_d = {
        "fio": fio,
        "birthdate": birthdate,
        "group": group,
        "gpa": gpa
    }
    
    validate_student(des_from_d)
    return des_from_d

def format_student(rec):
    #Обработка ФИО
    fio = rec["fio"]
    fio_split = fio.split()
    all_fio = fio_split[0].capitalize() +' '+ ''.join([x[0].upper()+'.' for x in fio_split[1:]])
    
    group = f"({rec['group']})"
    gpa = f"GPA {rec['gpa']}"
    age = f"{student_age(rec)} лет"
    
    return all_fio + ' ' + group + ', ' + age + ', ' + gpa
    
    


          
    
           