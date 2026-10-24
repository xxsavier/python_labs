# **Лабораторные работы по программированию на Python**
 
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Labs](https://img.shields.io/badge/labs-5%20of%2010-blue)
![stdlib](https://img.shields.io/badge/stack-stdlib%20%2B%20openpyxl-success)
 
</div>

## Навигация
 
| № | Тема | Что отработано | Код |
|:-:|---|---|---|
| **ЛР1** | Ввод/вывод и форматирование | `input`, `print`, f-строки, циклы | [`src/lab01`](src/lab01) |
| **ЛР2** | Коллекции и матрицы | `list`, `tuple`, `set`, `dict`, 2D-списки | [`src/lab02`](src/lab02) |
| **ЛР3** | Тексты и частоты слов | нормализация, регулярные выражения, словари | [`src/lab03`](src/lab03), [`src/lib/text.py`](src/lib/text.py) |
| **ЛР4** | Файлы TXT/CSV | `pathlib`, кодировки, `csv`, `argparse` | [`src/lab04`](src/lab04) |
| **ЛР5** | JSON и конвертации | `json`, `DictReader`/`DictWriter`, `openpyxl` | [`src/lab05`](src/lab05) |
 
## Структура репозитория
 
```text
python_labs/
├─ README.md
├─ requirements.txt        # openpyxl (ЛР5)
├─ src/
│  ├─ lib/text.py          # переиспользуемый модуль (ЛР3)
│  ├─ lab01 … lab05/       # решения по лабораторным
├─ data/                   # входные файлы и результаты (lab04, samples, out)
└─ images/                 # скриншоты запусков
```
 
## Быстрый старт
 
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
 
> [!NOTE]
> Все команды выполняются из корня репозитория. Файлы данных хранятся в UTF-8; при просмотре в PowerShell используйте `Get-Content файл -Encoding UTF8`.
 
## ЛР1. Ввод/вывод и форматирование
 
**Цель:** создать репозиторий с нужной структурой, познакомиться с Visual Studio Code и реализовать базовые программы.
 
**Реализовано:** приветствие по имени и возрасту, сумма и среднее двух чисел, расчёт цены со скидкой и НДС, перевод минут в `ч:мм`, инициалы из ФИО, подсчёт значений `True`/`False`, расшифровка строки по правилу.
 
<details>
<summary>Код src/lab01</summary>

```python

name = input('Имя: ')
age = int(input('Возраст: '))
print(f'Привет, {name}! Через год тебе будет {age+1}.')

a = float(input('a: ').replace(',', '.'))
b = float(input('b: ').replace(',', '.'))
summ = a+b
avg = round(summ/2,2)
print(f'sum={round(summ,2)}; avg={avg}')
 
price = float(input('price='))
discount = float(input('discount='))
vat = float(input('vat='))
 
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
 
print(f'База после скидки: {base:.2f} ₽')
print(f'НДС:               {vat_amount:.2f} ₽')
print(f'Итого к оплате:    {total:.2f} ₽')
 
minutes = int(input('Минуты: '))
hours = minutes//60
minutes = minutes%60
print(f'{hours}:{minutes:02d}')
 
fio = input('ФИО: ')
fio = ' ' + fio
initials = ''.join([fio[x].upper() for x in range(1, len(fio)) if fio[x].isalpha() and  not fio[x-1].isalpha()])
len_fio = len([x for x in fio if x != ' '])+2
print(f'Инициалы: {initials}.')
print(f'Длина (символов): {len_fio}')
 
n = int(input('in_1: '))
a = 0
b = 0
for i in range(n):
    user = input(f'in_{i+2}: ')
    if user[-5:] == 'False': b += 1
    if user[-4:] == 'True': a += 1
print('out: ' + str(a) + ' ' + str(b))
 
in0 = input('in: ')
out = ''
first_letter = 0
for i in in0:
    if i.isupper():
        out += i
        first_letter = in0.index(i)
        break
in1 = in0[first_letter:]
flag = False
for i in in1:
    if flag:
        out += i
        difference = in0.index(i)-first_letter
        break
    if i.isdigit():
        flag = True
in2 = in1[difference:]
for i in range(len(in2)):
    if i%difference == 0 and i!=0:
        out+=in2[i]  
print(f'out: {out}')
```
 
</details>
 
## ЛР2. Коллекции и матрицы
 
**Цель:** освоить операции над списками, кортежами, множествами и словарями; работать с 2D-списками (транспонирование, суммы по строкам и столбцам); аккуратно форматировать текстовые представления записей.
 
| Файл | Функции |
|---|---|
| `arrays.py` | `min_max`, `unique_sorted`, `flatten` |
| `matrix.py` | `transpose`, `row_sums`, `col_sums` |
| `tuples.py` | `format_record` |
 
<details>
<summary>Код src/lab02/arrays.py</summary>

```python
def min_max(user_list):
    """
    Находит минимальный и максимальный элемент списка чисел
    In: принимает от пользователя list[float | int] (проверяет, действительно ли введен список)
    Out: возвращает tuple[float | int, float | int] - с минимальным и максимальным числом;
    Возвращает ошибку ValueError в случае некорректного ввода 
    """
    if not isinstance(user_list, list):
        return 'ValueError'
    try:
        min_el = max_el = user_list[0]
        for el in user_list:
            if el < min_el: min_el = el
            if el > max_el: max_el = el
        return tuple([min_el, max_el]) 
    except (IndexError, TypeError):
        return 'ValueError'     
test_data_mm = [[3, -1, 5, 5, 0], [42], [-5, -2, -9], [], [1.5, 2, 2.0, -3.1]]
for test in test_data_mm:
    print(min_max(test))
 
def unique_sorted(user_list):
    """
    Сортирует список по возрастанию, сохраняя только уникальные элементы
    In: принимает от пользователя list[float | int] (проверяет, действительно ли введен список)
    Out: возвращает list[float | int] c отсортированными уникальными элементами;
    Возвращает ошибку ValueError в случае некорректного ввода 
    """
    if not isinstance(user_list, list):
            return 'ValueError'
    user_list = list(set(user_list))
    sorted_user_list = [10**10]
    for user_digit in user_list:
        for place in range(len(sorted_user_list)):
            if user_digit < sorted_user_list[place]: 
                sorted_user_list.insert(place, user_digit)
                break
    return sorted_user_list[:-1]
test_data_us = [[3, 1, 2, 1, 3], [], [-1, -1, 0, 2, 2], [1.0, 1, 2.5, 2.5, 0]]
for test in test_data_us:
    print(unique_sorted(test))
 
def flatten(user_list):
    """
    Разворачивает список списков/кортежей в один плоский список (row-major order)
    In: принимает от пользователя list[list | tuple] (проверяет, действительно ли введен список со списками и кортежами)
    Out: Возвращает 'расплющенный' список с элементами из вложенных кортежей/списков;
    Возвращает ошибку TypeError в случае некорректного ввода
    """
    out_list = []
    try:
        for list_i in user_list:
            if isinstance(list_i, tuple) or isinstance(list_i, list):
                for element in list_i:
                    out_list.append(element)
            else: raise TypeError
        return out_list
    except TypeError:
        return 'TypeError'
test_data_f = [[[1, 2], [3, 4]], [[1, 2], (3, 4, 5)], [[1], [], [2, 3]], [[1, 2], "ab"]]
for test in test_data_f:
    print(flatten(test))
```
 
</details>

<details>
<summary>Код src/lab02/matrix.py</summary>

```python
def transpose(matrix):
    """
    Реализует транспонирование матрицы
    In: принимает от пользователя list[list[float | int]] (проверяет, действительно ли введен список)
    Out: возвращает list[list] - транспонированную матрицу;
    Возвращает ValueError в случае некорректного ввода
    """
    if not isinstance(matrix, list):
            return 'ValueError'
    if len(matrix) > 0:
        rows = len(matrix[0])
        t_matrix = []
    else: return '[]'
    try:
        for number_element in range(rows):
            new_row = []
            for row in matrix:
                new_row.append(row[number_element])
            t_matrix.append(new_row)
        return t_matrix
    except IndexError:
        return 'ValueError'
test_data_t = [[[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4]], [], [[1, 2], [3]]]
for test in test_data_t:
    print(transpose(test))
 
def row_sums(user_list):
    """
    Находит сумму по каждой строке матрицы
    In: принимает от пользователя list[list[float | int]] (проверяет, действительно ли введен список)
    Out: возвращает list[float] - список с суммами по строкам;
    Возвращает ValueError в случае некорректного ввода
    """
    if not isinstance(user_list, list):
            return 'ValueError'
    list_with_sum = []
    try:
        len_row = len(user_list[0])
        for row in range(len(user_list)):
            sum_row = 0
            for ind in range(len_row):
                sum_row += user_list[row][ind]
            list_with_sum.append(sum_row)
        return list_with_sum
    except IndexError:
        return 'ValueError'
test_data_rs = [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]], [[1, 2], [3]]]
for test in test_data_rs:
    print(row_sums(test))
 
def col_sums(user_list):
    """
    Находит сумму по каждому столбцу матрицы
    In: принимает от пользователя list[list[float | int]] (проверяет, действительно ли введен список)
    Out: возвращает list[float] - список с суммами по столбцам;
    Возвращает ValueError в случае некорректного ввода
    """
    if not isinstance(user_list, list):
            return 'ValueError'
    list_with_sum = []
    try:
        len_row = len(user_list[0])
        for ind in range(len_row):
            sum_col = 0
            for row in range(len(user_list)):          
                sum_col += user_list[row][ind]
            list_with_sum.append(sum_col)
        return list_with_sum
    except IndexError:
        return 'ValueError'
test_data_cs = [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]], [[1, 2], [3]]]
for test in test_data_cs:
    print(col_sums(test))
```
 
</details>

<details>
<summary>Код src/lab02/tuples.py</summary>

```python
def format_record(user_tuple):
    """
    Реализует необходимую функцию, преобразующую кортеж в строку установленного вида
    In: принимает от пользователя tuple[str, str, float] (проверяет, действительно ли введен кортеж)
    Out: возвращает str - строку с информацией о студенте;
    Возвращает ошибку ValueError в случае некорректного ввода(неверный тип GPA, пустое ФИО, пустая группа) 
    """
    if not isinstance(user_tuple, tuple):
        return 'ValueError'
    try:
        fio = user_tuple[0]
        group = user_tuple[1]
        gpa = user_tuple[2]
        if len(user_tuple) > 3:
            raise ValueError
        # Обработка ФИО
        name_surname_fat = fio.split()
        if len(name_surname_fat) == 3: fio = name_surname_fat[0][0].upper() + name_surname_fat[0][1:] + ' ' + name_surname_fat[1][0].upper() + '.' + name_surname_fat[2][0].upper() +'.'
        else: fio = name_surname_fat[0] + ' ' + name_surname_fat[1][0].upper() + '.'
        # Обработка группы
        if len(group) == 0:
            raise ValueError
        group = 'гр. ' + group
        # Обработка GPA
        if int(gpa) > 5 or int(gpa) < 0:
            raise ValueError
        gpa = f'GPA {gpa:.2f}'
        return fio + ', ' + group + ', ' + gpa
    except IndexError:
        return "ValueError"
data = [("Иванов Иван Иванович", "BIVT-25", 4.6), ("Петров Пётр", "IKBO-12", 5.0), ("Петров Пётр Петрович", "IKBO-12", 5.0), ("  сидорова  анна   сергеевна ", "ABB-01", 3.999)]
for test in data:
    try: print(format_record(test))
    except ValueError: print('ValueError')
```
 
</details>
 
## ЛР3. Тексты и частоты слов
 
**Цель:** нормализация текста, аккуратная токенизация, подсчёт частот слов и вывод топ-N. Работа продолжает ЛР2 и готовит базу для ЛР4: модуль `lib/text.py` переиспользуется дальше.
 
| Функция | Назначение |
|---|---|
| `normalize` | `casefold`, замена `ё`→`е`, схлопывание пробелов |
| `tokenize` | разбиение на слова по шаблону `\w+(-\w+)*` |
| `count_freq` | словарь частот слов |
| `top_n` | топ-N: частота по убыванию, при равенстве слово по алфавиту |
 
```powershell
"Привет, мир! Привет!!!" | python -m src.lab03.text_stats
```
 
<details>
<summary>Код src/lib/text.py</summary>

```python
import re
 
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    '''
    Функция нормализует введенные текстовые данные
    Принимает на вход текстовые данные, две булевых переменных:
        casefold: True - приводит к casefold / False - использует lower()
        yo2e: True - заменяет Ё(ё) на Е(е) / False - оставляет Ё(ё)
    Возвращает текст приведенный к необходимому формату
    '''
    if casefold: text = text.casefold()
    else: text = text.lower()
    if yo2e: text = text.replace('ё', 'е')
    text = ' '.join(text.split())
    return text
 
def tokenize(text: str) -> list[str]:
    '''
    Функция разбивает введенный текст по небуквенно-цифровым разделителям
    Принимает на вход текстовые данные
    Возвращает список со словами(последовательностями символов \w + [-] в сложных словах
    '''
    our_alphas = re.finditer(r'\w+(-\w+)*', text)
    words = []
    for alphas in our_alphas:
        words.append(alphas.group())
    return words
 
def count_freq(tokens: list[str]) -> dict[str, int]:
    '''
    Функция считает частоты введенных значений в списке
    Принимает список с текстовыми элементами
    Возвращает словарь типа: {'елемент': частота появлений в списке}
    '''
    freq = dict()
    for element in tokens:
        if element not in freq: freq[element] = 1
        else: freq[element] += 1
    return dict(sorted(freq.items()))
 
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    '''
    Функция возвращает топ-N по убыванию частоты; при равенстве — по алфавиту слова
    Принимает словарь с элементами и их частотами, число N - количество возвращаемых ТОП-элементов
    Возвращает отсортрованный список ТОП-N элементов с кортежами
    '''
    freqs = sorted(freq.items(), key = lambda x: (-x[1], x[0]))[:n]
    return freqs
```
 
</details>

<details>
<summary>Код src/lab03/text_stats.py</summary>

```python
import sys
sys.stdin.reconfigure(encoding='utf-8')
 
from src.lib.text import normalize, tokenize, count_freq, top_n
 
'''
Меняет кодировку на utf-8 для корректной работы с входными данными через sys.stdin.reconfigure(encoding='utf-8')
Получает данные через sys.stdin.read() - текст
Возвращает общее количество слов в введенном тексте, количество уникальных слов;
и Топ-5 наиболее частых слов (при константе excel == True: красивый табличный вывод / excel == False: базовый вывод)
'''
 
excel = True
 
text = sys.stdin.read()
text = normalize(text)
tokens = tokenize(text)
 
print(f'Всего слов: {len(tokens)}')
print(f'Уникальных слов: {len(set(tokens))}')
print('Топ-5:')
 
if not excel:
    top = top_n(count_freq(tokens))
    for word, freq in top:
        print(f'{word}:{freq}')
 
if excel:
    top = top_n(count_freq(tokens))
    max_len = max(max([len(word[0]) for word in top])+1, 6)
    
    first_row = 'слово' + (max_len-5)*' ' + '|' +'  частота'
    print(first_row)
    print('-'*len(first_row))
    for word, freq in top:
            print(word + (max_len-len(word))*' ' + '| ' + str(freq))
    print('...')
```
 
</details>
 
## ЛР4. Файлы: TXT/CSV и отчёты по текстовой статистике
 
**Цель:** закрепить работу с файлами (чтение и запись, кодировки), автоматизировать сбор статистики по словам и выгружать её в CSV. Модуль `src/lib/text.py` из ЛР3 используется повторно.
 
**Реализовано:**
 
- `io_txt_csv.py`: `read_text` (UTF-8 по умолчанию), `write_csv` (проверка длины строк), `ensure_parent_dir`;
- `text_report.py`: отчёт `word,count`, параметры `--in`, `--out`, `--encoding`;
- ★ несколько файлов: отчёты `--per-file` и `--total`, таблица в консоли;
- обработка ошибок: нет файла и неверная кодировка дают понятное сообщение и код выхода 1; пустой вход даёт CSV только с заголовком.

```powershell
python src/lab04/text_report.py
python src/lab04/text_report.py --in data/lab04/cp1251.txt --encoding cp1251
python src/lab04/text_report.py --in data/lab04/a.txt data/lab04/b.txt --per-file data/lab04/report_per_file.csv --total data/lab04/report_total.csv
```
 
<details>
<summary>Код src/lab04/text_report.py</summary>

```python
from __future__ import annotations
 
import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
 
# чтобы работали импорты "from lib.text import ..." при запуске из корня репозитория
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
from lib.text import normalize, tokenize, count_freq, top_n  # из ЛР3
from io_txt_csv import read_text, write_csv
 
 
def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    """Возвращает все пары (слово, число) в нужном порядке.
 
    Порядок: count по убыванию, при равенстве слово по возрастанию.
 
    Args:
        freq: словарь {слово: частота}.
    """
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
 
 
def load_tokens(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """Читает файл и превращает его текст в список слов.
 
    Ошибки чтения (FileNotFoundError, UnicodeDecodeError) не перехватываются.
 
    Args:
        path: путь к текстовому файлу.
        encoding: кодировка файла.
 
    Returns:
        Список слов после нормализации и токенизации.
    """
    return tokenize(normalize(read_text(path, encoding=encoding)))
 
 
def print_table(
    rows: Sequence[tuple[str, int]],
    header: tuple[str, str] = ("word", "count"),
) -> None:
    """Печатает таблицу в консоль, ширина столбцов по самому длинному значению (★).
 
    Args:
        rows: пары (слово, число).
        header: заголовки двух столбцов.
    """
    data = [header] + [(word, str(count)) for word, count in rows]
    width_word = max(len(row[0]) for row in data)
    width_count = max(len(row[1]) for row in data)
    for i, (word, count) in enumerate(data):
        print(f"{word:<{width_word}} | {count:<{width_count}}")
        if i == 0:
            print("-" * width_word + "-+-" + "-" * width_count)
 
 
def parse_args() -> argparse.Namespace:
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов в текстовых файлах")
    parser.add_argument("--in", dest="inputs", nargs="+", default=["data/lab04/input.txt"],
                        help="один или несколько входных файлов")
    parser.add_argument("--out", default="data/lab04/report.csv",
                        help="выходной CSV word,count")
    parser.add_argument("--encoding", default="utf-8",
                        help="кодировка входных файлов (например cp1251)")
    parser.add_argument("--per-file", default=None,
                        help="★ CSV file,word,count по каждому файлу")
    parser.add_argument("--total", default=None,
                        help="★ сводный CSV word,count по всем файлам")
    return parser.parse_args()
 
 
def main() -> None:
    """Читает файлы, считает частоты, пишет CSV-отчёты и печатает резюме."""
    args = parse_args()
 
    all_tokens: list[str] = []
    per_file_rows: list[tuple[str, str, int]] = []
 
    for path in args.inputs:
        try:
            tokens = load_tokens(path, encoding=args.encoding)
        except FileNotFoundError:
            print(f"Ошибка: файл не найден: {path}")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Ошибка: не удалось прочитать {path} в кодировке {args.encoding}. "
                  f"Попробуйте указать другую, например --encoding cp1251")
            sys.exit(1)
 
        all_tokens.extend(tokens)
 
        freq_file = count_freq(tokens)
        name = Path(path).name
        for word, count in sorted_word_counts(freq_file):
            per_file_rows.append((name, word, count))
 
    freq = count_freq(all_tokens)
    rows = sorted_word_counts(freq)
 
    # базовый отчёт (при одном входном файле это отчёт по нему)
    write_csv(rows, args.out, header=("word", "count"))
 
    # ★ отчёт по каждому файлу: file ↑, count ↓, word ↑
    if args.per_file:
        per_file_rows.sort(key=lambda r: (r[0], -r[2], r[1]))
        write_csv(per_file_rows, args.per_file, header=("file", "word", "count"))
 
    # ★ сводный отчёт по всем файлам
    if args.total:
        write_csv(rows, args.total, header=("word", "count"))
 
    print(f"Всего слов: {len(all_tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")
    for word, count in top_n(freq, 5):
        print(f"{word}:{count}")
 
    print()
    print_table(rows)
 
 
if __name__ == "__main__":
    main()
```
 
</details>
 
## ЛР5. JSON и конвертации (JSON↔CSV, CSV→XLSX)
 
**Цель:** разобраться с форматом JSON, сериализацией и десериализацией, табличными конвертациями. Работа продолжает ЛР4 и готовит базу для ЛР6 (CLI-конвертеры) и ЛР7 (тестирование).
 
**Реализовано:**
 
| Модуль | Функция | Что делает |
|---|---|---|
| `json_csv.py` | `json_to_csv` | список словарей из JSON в CSV; пропущенные поля становятся пустыми |
| `json_csv.py` | `csv_to_json` | CSV с заголовком в JSON; значения остаются строками |
| `csv_xlsx.py` | `csv_to_xlsx` | CSV в XLSX (`openpyxl`), лист `Sheet1`, автоширина колонок от 8 символов |
 
**Валидация:** неверный тип файла, пустой JSON или CSV и неподдерживаемая структура дают `ValueError`; отсутствующий файл даёт `FileNotFoundError`. Кодировка везде UTF-8, модули ничего не выводят в консоль.
 
**Допущения:** порядок колонок как в первом объекте, затем новые ключи в порядке появления; при CSV → JSON типы не сохраняются (все значения строки); вложенные структуры не поддерживаются.
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/samples/people.json','data/out/people_from_json.csv')"
python -c "from src.lab05.json_csv import csv_to_json; csv_to_json('data/samples/people.csv','data/out/people_from_csv.json')"
python -c "from src.lab05.csv_xlsx import csv_to_xlsx; csv_to_xlsx('data/samples/people.csv','data/out/people.xlsx')"
```
 
Собственные примеры (тема ЦСКА): `cska_players.json` для JSON → CSV, `cska_players.csv` для CSV → JSON, `cska_matches.csv` для CSV → XLSX.
 
<details>
<summary>Код src/lab05/json_csv.py</summary>

```python
from __future__ import annotations
 
import csv
import json
from pathlib import Path
 
MSG_BAD_JSON = "Пустой JSON или неподдерживаемая структура"
 
 
def is_list_of_dicts(data) -> bool:
    """True, если data это список словарей, среди которых есть непустой."""
    return (
        isinstance(data, list)
        and all(isinstance(item, dict) for item in data)
        and any(data)
    )
 
 
def check_suffix(path: str | Path, suffix: str) -> None:
    """Проверяет расширение файла, иначе ValueError."""
    if Path(path).suffix.lower() != suffix:
        raise ValueError(
            f"Неверный тип файла: ожидается {suffix}, "
            f"получен {Path(path).suffix or 'без расширения'}"
        )
 
 
def json_to_csv(json_path: str | Path, csv_path: str | Path) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.
 
    Колонки: ключи первого объекта, затем новые ключи из следующих объектов
    в порядке появления. Отсутствующие поля заполняются пустыми строками.
    Кодировка UTF-8.
 
    Raises:
        ValueError: неверный тип файла, пустой JSON, не список словарей.
        FileNotFoundError: JSON-файл не найден.
    """
    check_suffix(json_path, ".json")
    check_suffix(csv_path, ".csv")
 
    text = Path(json_path).read_text(encoding="utf-8")
 
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(MSG_BAD_JSON) from None
 
    if not is_list_of_dicts(data):
        raise ValueError(MSG_BAD_JSON)
 
    fieldnames = list(dict.fromkeys(key for item in data for key in item))
 
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(csv_path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(data)
 
 
def csv_to_json(csv_path: str | Path, json_path: str | Path) -> None:
    """Преобразует CSV (с заголовком) в JSON: список словарей.
 
    Все значения сохраняются как строки. Кодировка UTF-8.
 
    Raises:
        ValueError: неверный тип файла, пустой CSV, нет заголовка или данных.
        FileNotFoundError: CSV-файл не найден.
    """
    check_suffix(csv_path, ".csv")
    check_suffix(json_path, ".json")
 
    with Path(csv_path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, restval="")
        if not reader.fieldnames:
            raise ValueError("CSV без заголовка или пустой")
        rows = list(reader)
 
    if not rows:
        raise ValueError("В CSV нет строк данных")
 
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(json_path).open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
```
 
</details>

<details>
<summary>Код src/lab05/csv_xlsx.py</summary>

```python
from __future__ import annotations
 
import csv
from pathlib import Path
 
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
 
MIN_COLUMN_WIDTH = 8
 
 
def csv_to_xlsx(csv_path: str | Path, xlsx_path: str | Path) -> None:
    """Конвертирует CSV в XLSX (через openpyxl).
 
    Первая строка CSV это заголовок. Лист называется "Sheet1".
    Ширина колонки равна длине самого длинного текста в ней,
    но не меньше 8 символов. Кодировка CSV: UTF-8.
 
    Raises:
        ValueError: неверный тип файла или пустой CSV.
        FileNotFoundError: CSV-файл не найден.
    """
    if Path(csv_path).suffix.lower() != ".csv":
        raise ValueError("Входной файл должен иметь расширение .csv")
    if Path(xlsx_path).suffix.lower() != ".xlsx":
        raise ValueError("Выходной файл должен иметь расширение .xlsx")
 
    with Path(csv_path).open(encoding="utf-8", newline="") as f:
        rows = [row for row in csv.reader(f) if row]
 
    if not rows:
        raise ValueError("CSV пустой")
 
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    for row in rows:
        sheet.append(row)
 
    columns_count = max(len(row) for row in rows)
    for index in range(columns_count):
        longest = max(
            (len(row[index]) for row in rows if index < len(row)),
            default=0,
        )
        letter = get_column_letter(index + 1)
        sheet.column_dimensions[letter].width = max(MIN_COLUMN_WIDTH, longest)
 
    Path(xlsx_path).parent.mkdir(parents=True, exist_ok=True)
    workbook.save(xlsx_path)
```
 
</details>
 
<div align="center">
 
</div>
 
