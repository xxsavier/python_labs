import argparse
import sys
from pathlib import Path

from src.lab05.json_csv import csv_to_json, json_to_csv
from src.lab05.csv_xlsx import csv_to_xlsx


def main():
    """
    Конвертирует файлы (json <-> csv, csv -> xlsx)
    
    Подкоманды:
        csv2json --in Путь к исходному файлу --out Путь к файлу записи
            Конвертация csv -> json
        json2csv --in Путь к исходному файлу --out Путь к файлу записи
            Конвертация json -> csv
        csv2xlsx --in Путь к исходному файлу --out Путь к файлу записи
            Конвертация csv -> xlsx

    Файлы читаются в кодировке UTF-8. Результат выводится в stdout,
    сообщения об ошибках в stderr.
    
    Raises:
        SystemExit: код 2, если аргументы неверны (подкоманда не указана,
            нет --in, нет --out);
            код 1, если файл не найден (FileNotFoundError), не в UTF-8
            (UnicodeDecodeError) или не удалось его прочитать (OSError:
            путь указывает на папку, нет прав доступа и т. п.).
    """
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    subparser = parser.add_subparsers(dest="function", required=True)

    function1 = subparser.add_parser("csv2json", help="Конвертер из csv в json")
    function1.add_argument("--in", dest="input", required=True, help="Путь к файлу csv")
    function1.add_argument("--out", dest="output", required=True, help="Путь к файлу json")

    function2 = subparser.add_parser("json2csv", help="Конвертер из json в csv")
    function2.add_argument("--in", dest="input", required=True, help="Путь к файлу json")
    function2.add_argument("--out", dest="output", required=True, help="Путь к файлу csv")

    function3 = subparser.add_parser("csv2xlsx", help="Конвертер из csv в xlsx")
    function3.add_argument("--in", dest="input", required=True, help="Путь к файлу csv")
    function3.add_argument("--out", dest="output", required=True, help="Путь к файлу xlsx")

    args = parser.parse_args()

    try:
        if args.function == "csv2json":
            csv_to_json(args.input, args.output)
        elif args.function == "json2csv":
            json_to_csv(args.input, args.output)
        elif args.function == "csv2xlsx":
            csv_to_xlsx(args.input, args.output)
        
    except FileNotFoundError:
        print(f'Не найден файл. Проверьте пути к файлам: "{args.input}"; "{args.output}". Ошибка FileNotFoundError.', file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка: файл '{args.input}' не является UTF-8 текстом. Ошибка UnicodeDecodeError.", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f'Ошибка {e}. Проверьте пути к файлам: "{args.input}"; "{args.output}".', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
