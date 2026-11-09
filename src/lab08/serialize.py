from datetime import date
def student_age(rec, today=None):
    today = today or date.today()
    birthday = date.fromisoformat(rec["birthdate"])
    minus_year = 0
    if today.month <= birthday.month and today.day < birthday.day:
        minus_year += 1
    return today.year - birthday.year - minus_year

its = {"fio": "Степанов Степан Степанович", "birthdate": "2007-11-08", "group": "БИВТ-25-2","gpa": 3.7 }
print(student_age(its))