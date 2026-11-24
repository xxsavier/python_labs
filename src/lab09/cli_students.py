"""
Модуль командной строки для управления базой данных студентов.

Позволяет добавлять, просматривать, искать, удалять и обновлять
записи студентов в CSV-хранилище.
"""

import argparse
import csv
import sys

from src.lab08.models import format_student, make_student
from src.lab09.group import (
    add_student,
    find_students,
    list_students,
    remove_student,
    update_student, 
)

def build_parser():
    """
    Создает и настраивает парсер аргументов командной строки.

    Добавляет общие параметры и подкоманды:
    add, list, find, remove и update.

    Returns:
        argparse.ArgumentParser: Настроенный парсер аргументов.
    """
    parser = argparse.ArgumentParser(description="CLI для работы с базой студентов")
    parser.add_argument("--db", default="data/lab09/students.csv", help="Путь к CSV-хранилищу")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Добавить студента")
    add_parser.add_argument("--db", default=argparse.SUPPRESS, help="Путь к CSV-хранилищу")
    add_parser.add_argument("--fio", required=True, help="ФИО студента")
    add_parser.add_argument("--birthdate", required=True, help="Дата рождения студента")
    add_parser.add_argument("--group", required=True, help="Группа студента")
    add_parser.add_argument("--gpa", required=True, help="GPA студента")

    list_parser = subparsers.add_parser("list", help="Вывести список студентов")
    list_parser.add_argument("--db", default=argparse.SUPPRESS, help="Путь к CSV-хранилищу")
    list_parser.add_argument("--sort", choices=("fio", "gpa"), help="Поле сортировки")

    find_parser = subparsers.add_parser("find", help="Найти студентов по части ФИО")
    find_parser.add_argument("--db", default=argparse.SUPPRESS, help="Путь к CSV-хранилищу")
    find_parser.add_argument("--q", required=True, help="Подстрока для поиска в ФИО")

    remove_parser = subparsers.add_parser("remove", help="Удалить студента по ФИО")
    remove_parser.add_argument("--db", default=argparse.SUPPRESS, help="Путь к CSV-хранилищу")
    remove_parser.add_argument("--fio", required=True, help="ФИО студента")

    update_parser = subparsers.add_parser("update", help="Обновить данные студента")
    update_parser.add_argument("--db", default=argparse.SUPPRESS, help="Путь к CSV-хранилищу")
    update_parser.add_argument("--fio", required=True, help="ФИО студента для поиска")
    update_parser.add_argument("--birthdate", help="Новая дата рождения")
    update_parser.add_argument("--group", help="Новая группа")
    update_parser.add_argument("--gpa", help="Новый GPA")

    return parser


def main():
    """
    Выполняет команду, переданную пользователем через терминал.

    Обрабатывает аргументы, вызывает соответствующие функции
    для работы с базой студентов и выводит результат.

    Returns:
        int: Код завершения программы (0 — успех, 1 — ошибка).
    """
    args = build_parser().parse_args()

    try:
        if args.command == "add":
            student = make_student(args.fio, args.birthdate, args.group, parse_gpa(args.gpa))
            add_student(args.db, student)
            print("Студент добавлен.")
        elif args.command == "list":
            for student in list_students(args.db, args.sort):
                print(format_student(student))
        elif args.command == "find":
            students = find_students(args.db, args.q)
            if not students:
                print("Не найден соответствующий студент.")
            else:
                for student in students:
                    print(format_student(student))
        elif args.command == "remove":
            removed = remove_student(args.db, args.fio)
            print(f"Удалено: {removed}")
        elif args.command == "update":
            fields = {
                field: value
                for field, value in (
                    ("birthdate", args.birthdate),
                    ("group", args.group),
                    ("gpa", parse_gpa(args.gpa) if args.gpa is not None else None),
                )
                if value is not None
            }
            updated = update_student(args.db, args.fio, **fields)
            if updated:
                print("Данные студента обновлены.")
            else:
                print("Студент не найден.")
    except (ValueError, OSError, UnicodeError, csv.Error) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    return 0


def parse_gpa(value):
    """
    Преобразует переданное значение GPA в число с плавающей точкой.

    Args:
        value: Значение GPA, полученное из аргументов командной строки.

    Returns:
        float: Преобразованное числовое значение GPA.

    Raises:
        ValueError: Если переданное значение нельзя преобразовать в число.
    """
    try:
        return float(value)
    except (ValueError, TypeError) as error:
        raise ValueError(f"GPA должно быть числом, получено {value!r}") from error


if __name__ == "__main__":
    raise SystemExit(main())
