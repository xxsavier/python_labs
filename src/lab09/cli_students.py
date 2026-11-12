import argparse

parser = argparse.ArgumentParser(description="CLI-утилиты для работы с хранилищем; lab09")
parser.add_argument("--db", default="data/lab09/students.csv", help="Путь к  необходимому хранилищу")
subparsers = parser.add_subparsers(dest="command", required="True")

add_pars = subparsers.add_parser("add", help="Запись студента в конец")
add_pars.add_argument("--fio", required=True, help="ФИО студента")
add_pars.add_argument("--birthdate", required=True, help="Дата рождения студента")
add_pars.add_argument("--group", required=True, help="Группа студента")
add_pars.add_argument("--gpa", type=float, required=True, help="GPA студента")

list_pars = subparsers.add_parser("list", help="Выводит список всех студентов")
list_pars.add_argument("--sort", help="По какому параметру сортировать")

find_pars = subparsers.add_parser("find", help="Поиск студентов по части ФИО")
find_pars.add_argument("--q", required=True, help = "Строка поиска")

remove_pars = subparsers.add_parser("remove", help="Удаляет студента по ФИО")
remove_pars.add_argument("--fio", required=True, help="ФИО студента")

update_pars = subparsers.add_parser("update", help="Обновить выбранное поле студента")
update_pars.add_argument("--fio", help="ФИО студента")
update_pars.add_argument("--birthdate", help="Дата рождения студента")
update_pars.add_argument("--group", help="Группа студента")
update_pars.add_argument("--gpa", type=float, help="GPA студента")

args = parser.parse_args()

if args.command == "X":
    pass