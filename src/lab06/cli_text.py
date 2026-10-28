import argparse
from pathlib import Path
import sys

from src.lib.text import normalize, tokenize, count_freq, top_n


def main():
    """
    1. Анализирует частоты слов в тексте, выводит ТОП-n слов (используются функции из lab03).
    2. Выводит содержимое файла построчно (с нумерацией при -n).
    
    Подкоманды:
        stats --input ПУТЬ [--top N]
            Печатает N самых частых слов файла (по умолчанию 5). Текст
            нормализуется и разбивается на слова функциями из src.lib.text.
        cat --input ПУТЬ [-n]
            Печатает файл построчно; с флагом -n строки нумеруются с 1.

    Файлы читаются в кодировке UTF-8. Результат выводится в stdout,
    сообщения об ошибках в stderr.
    
    Raises:
        SystemExit: код 2, если аргументы неверны (подкоманда не указана,
            нет --input, значение --top не число или не больше нуля);
            код 1, если файл не найден (FileNotFoundError), не в UTF-8
            (UnicodeDecodeError) или не удалось его прочитать (OSError:
            путь указывает на папку, нет прав доступа и т. п.).

    """
    parser = argparse.ArgumentParser(description="CLI-утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cat_parser = subparsers.add_parser("cat", help="Вывод содержимого файла построчно")
    cat_parser.add_argument("--input", required=True, help="Путь к файлу")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")
    
    stats_parser = subparsers.add_parser("stats", help="Анализ частот слов в тексте")
    stats_parser.add_argument("--input", required=True, help="Путь к файлу с текстом")
    stats_parser.add_argument("--top", type=int, default=5, help="Количество ТОП-элементов")

    args = parser.parse_args()

    try:
        if args.command == "stats":
            if args.top <= 0:
                stats_parser.error("Введите корректное значение top (>0)")
        
            with Path(args.input).open("r", encoding="utf-8") as f:
                text = f.read()
                token_text = tokenize(normalize(text))
                freq = count_freq(token_text)
                top_words = top_n(freq, args.top)
            print(f"Топ-{min(args.top, len(top_words))} слов:")
            place = 1
            for word, freq_for_word in top_words:
                print(f"{place}. {word} - {freq_for_word}")
                place += 1

        elif args.command == "cat":
            with Path(args.input).open("r", encoding="utf-8") as f:
                if args.n:
                    n = 1
                    for line in f:
                        line = line.strip("\n")
                        print(f'{n}. {line}')
                        n += 1
                else:
                    for line in f:
                        line = line.strip("\n")
                        print(line)
    except UnicodeDecodeError:
        print(f"Ошибка: файл '{args.input}' не является UTF-8 текстом. Ошибка UnicodeDecodeError.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f'Файл "{args.input}" не найден. Ошибка FileNotFoundError.', file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f'Ошибка {e}. Проверьте путь к файлу "{args.input}".', file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()