# Лабораторная работа 5. JSON и конвертации (JSON↔CSV, CSV→XLSX)

## Содержание
 
1. [Цель работы](#цель-работы)
2. [Подготовка и установка](#подготовка-и-установка)
3. [Задание A. Модуль json_csv.py](#задание-a-модуль-json_csvpy)
4. [Задание B. Модуль csv_xlsx.py](#задание-b-модуль-csv_xlsxpy)
5. [Допущения и принятые решения](#допущения-и-принятые-решения)
6. [Демонстрация работы](#демонстрация-работы)
## Цель работы
 
Разобраться с форматом JSON, сериализацией и десериализацией, а также с табличными конвертациями: JSON → CSV, CSV → JSON и CSV → XLSX. Работа продолжает ЛР4 (работа с файлами) и готовит базу для ЛР6 (CLI-конвертеры) и ЛР7 (тестирование). Кроме `openpyxl` (только для XLSX) используется стандартная библиотека: `json`, `csv`, `pathlib`.
 
## Подготовка и установка
 
Все команды выполняются из корня репозитория (`python_labs`) в терминале с активным виртуальным окружением. Нужен Python 3.9 или новее.
 
```powershell
pip install -r requirements.txt
```
 
Содержимое `requirements.txt`:
 
```text
openpyxl>=3.1
```
 
Используемые инструменты:
 
| Модуль | Что применяется |
|---|---|
| `json` | `json.loads` (строка в объект), `json.dump(..., ensure_ascii=False, indent=2)` (объект в файл) |
| `csv` | `csv.DictReader` (читает строки как словари), `csv.DictWriter` (пишет словари), `csv.reader` (читает строки как списки) |
| `pathlib` | `Path` для путей, чтения файла и создания папок |
| `openpyxl` | `Workbook`, `ws.append`, `ws.column_dimensions[...].width`, `wb.save` |
 
## Задание A. Модуль json_csv.py
 
Модуль содержит две основные функции и две вспомогательные. Модуль ничего не печатает: только работа с файлами и исключения.
 
| Функция | Что делает |
|---|---|
| `json_to_csv(json_path, csv_path)` | читает JSON (список словарей) и записывает CSV |
| `csv_to_json(csv_path, json_path)` | читает CSV с заголовком и записывает JSON (список словарей) |
| `check_suffix(path, suffix)` | проверяет расширение файла, иначе `ValueError` |
| `is_list_of_dicts(data)` | проверяет, что данные это список словарей, среди которых есть непустой |

<details>
<summary>Код src/lab05/json_csv.py</summary>

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

def is_list_of_dicts(data) -> bool:
    """True, если data это список словарей, среди которых есть непустой."""
    return isinstance(data, list) and all(isinstance(dict_x, dict) for dict_x in data) and any(data)


def check_suffix(path: str | Path, suffix: str) -> None:
    """Проверяет расширение файла, иначе ValueError."""
    if Path(path).suffix.lower() != suffix:
        raise ValueError(f"Неверный тип файла: ожидается {suffix}, получен {Path(path).suffix or 'без расширения'}")


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.

    Колонки: ключи первого объекта, затем новые ключи из следующих объектов
    в порядке появления. Отсутствующие поля заполняются пустыми строками.
    Кодировка UTF-8.

    Raises:
        ValueError: неверный тип файла, пустой JSON, не список словарей.
        FileNotFoundError: JSON-файл не найден.
    """
    check_suffix(json_path, '.json')
    check_suffix(csv_path, '.csv')

    data = Path(json_path).read_text(encoding="utf-8")

    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Пустой JSON или неподдерживаемая структура") from None
    if not is_list_of_dicts(data): 
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    fieldnames = list(dict.fromkeys(key for item in data for key in item))

    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(csv_path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
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

## Задание B. Модуль csv_xlsx.py

<details>
<summary>Код src/lab05/csv_xlsx.py</summary>

```python
from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.utils import get_column_letter


def csv_to_xlsx(csv_path: str | Path, xlsx_path: str | Path) -> None:
    """Конвертирует CSV в XLSX (openpyxl).

    Первая строка CSV это заголовок. Лист называется "Sheet1".
    Ширина колонки равна длине самого длинного текста в ней, но не меньше 8.

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

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    for row in rows:
        ws.append(row)

    n_cols = max(len(row) for row in rows)
    for col in range(n_cols):
        longest = max((len(row[col]) for row in rows if col < len(row)), default=0)
        ws.column_dimensions[get_column_letter(col + 1)].width = max(8, longest)

    Path(xlsx_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path)
```
 
</details>

## Допущения и принятые решения
 
| Вопрос | Решение |
|---|---|
| Порядок колонок в `json_to_csv` | как в первом объекте, затем новые ключи из следующих объектов в порядке первого появления |
| Отсутствующие поля в объекте | заполняются пустой строкой (`restval=""`) |
| Типы значений при CSV → JSON | все значения остаются строками (`"22"`, а не `22`), как требует задание; поэтому цепочка JSON → CSV → JSON не сохраняет числа |
| Значения `None` и числа при JSON → CSV | числа записываются текстом, `null` становится пустой клеткой |
| Вложенные объекты и списки в JSON | не поддерживаются, в CSV попадёт их текстовая запись |
| CSV только с заголовком | в `csv_to_json` считается пустым (`ValueError`); в `csv_to_xlsx` пустым считается только файл без строк |
| Пустые строки внутри CSV при конвертации в XLSX | пропускаются |
| Кодировка | строго UTF-8 для всех файлов; файлы должны быть сохранены без BOM |
| Пути | относительные, от корня репозитория |
| Лист XLSX | называется `Sheet1` |
| Ширина колонок XLSX | по самому длинному значению в колонке, но не меньше 8 символов |
| Вывод в консоль из модулей | отсутствует: функции только работают с файлами и поднимают исключения |
| Внешние пакеты | только `openpyxl` (по условию), остальное стандартная библиотека | 
 
## Демонстрация работы
 
Все команды выполняются из корня репозитория. Просмотр CSV и JSON в PowerShell делается с параметром `-Encoding UTF8`, иначе русские буквы отображаются неправильно (файлы при этом записаны верно).
 
### Сценарий 1. JSON → CSV
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/samples/people.json','data/out/people_from_json.csv')"
Get-Content data\out\people_from_json.csv -Encoding UTF8
```
 
Ожидаемый результат: заголовок `name,age,city` и четыре строки данных.
 
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
Анна,21,Омск
Дмитрий,30,Москва
```
 
**Скриншот 1.** Вывод команд выше: запуск и содержимое `people_from_json.csv`.

![Скриншот 1: JSON → CSV, содержимое people_from_json.csv](../../images/lab05/image01.png)

### Сценарий 2. CSV → JSON
 
```powershell
python -c "from src.lab05.json_csv import csv_to_json; csv_to_json('data/samples/people.csv','data/out/people_from_csv.json')"
Get-Content data\out\people_from_csv.json -Encoding UTF8
```
 
Ожидаемый результат: список из четырёх объектов с теми же ключами `name`, `age`, `city`; значения строки.
 
**Скриншот 2.** Содержимое `people_from_csv.json`.

![Скриншот 2: CSV → JSON, содержимое people_from_csv.json](../../images/lab05/image02.png)

### Проверка количества записей
 
```powershell
(Get-Content data\out\people_from_json.csv).Count
python -c "import json; print(len(json.load(open('data/out/people_from_csv.json', encoding='utf-8'))))"
```
 
Первая команда выводит 5 (заголовок и 4 записи), вторая выводит 4. В исходных `people.json` и `people.csv` тоже по 4 записи, значит, при конвертации записи не теряются и не добавляются.
 
**Скриншот 3.** Вывод обеих команд.

![Скриншот 3: проверка количества записей](../../images/lab05/image03.png)

### Сценарий 3. CSV → XLSX
 
```powershell
python -c "from src.lab05.csv_xlsx import csv_to_xlsx; csv_to_xlsx('data/samples/people.csv','data/out/people.xlsx'); csv_to_xlsx('data/samples/cities.csv','data/out/cities.xlsx')"
```
 
Проверка вручную: открыть файлы в Excel или LibreOffice, убедиться, что лист называется `Sheet1`, первая строка заголовок, текст в колонках не обрезан, а ширина каждой колонки не меньше 8 символов.
 
**Скриншот 4.** `people.xlsx` в Excel или LibreOffice (видно название листа и колонки).

![Скриншот 4: people.xlsx](../../images/lab05/image05.png)
 
**Скриншот 5.** `cities.xlsx` в Excel или LibreOffice.

![Скриншот 5: cities.xlsx](../../images/lab05/image04.png)
 
### Собственные примеры (тема ЦСКА)
 
Для каждого сценария подготовлен свой набор данных.
 
**JSON → CSV на примере `cska_players.json`.** Данные намеренно неполные: у одного игрока нет года рождения, у другого страны. Недостающие поля становятся пустыми клетками.
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/samples/cska_players.json','data/out/cska_players_from_json.csv')"
Get-Content data\out\cska_players_from_json.csv -Encoding UTF8
```
 
Ожидаемый результат:
 
```csv
name,position,birth_year,country
Игорь Акинфеев,Вратарь,1986,Россия
Сергей Игнашевич,Защитник,1979,Россия
Василий Березуцкий,Защитник,1982,
Георгий Щенников,Защитник,,Россия
Алан Дзагоев,Полузащитник,1990,Россия
Вагнер Лав,Нападающий,1984,Бразилия
```
 
**Скриншот 6.** Запуск и содержимое `cska_players_from_json.csv` (видны пустые клетки).

![Скриншот 6: cska_players_from_json.csv](../../images/lab05/image06.png)
 
**CSV → JSON на примере `cska_players.csv`.**
 
```powershell
python -c "from src.lab05.json_csv import csv_to_json; csv_to_json('data/samples/cska_players.csv','data/out/cska_players_from_csv.json')"
Get-Content data\out\cska_players_from_csv.json -Encoding UTF8
```
 
**Скриншот 7.** Содержимое `cska_players_from_csv.json` (5 объектов, `birth_year` в виде строки).

![Скриншот 7: cska_players_from_csv.json](../../images/lab05/image07.png)
 
**CSV → XLSX на примере `cska_matches.csv`.** В колонке `comment` длинный текст, поэтому ширина колонки заметно больше остальных (автоширина). Данные в этом файле условные, они нужны только для демонстрации.
 
```powershell
python -c "from src.lab05.csv_xlsx import csv_to_xlsx; csv_to_xlsx('data/samples/cska_matches.csv','data/out/cska_matches.xlsx')"
```
 
Ожидаемые ширины колонок: A = 10, B = 9, C = 8, D = 8, E = 51.
 
**Скриншот 8.** `cska_matches.xlsx` в Excel или LibreOffice.

![Скриншот 8: cska_matches.xlsx](../../images/lab05/image08.png)
 
### Сценарий 4. Проверка ошибок
 
Для проверки временно создаются тестовые файлы в `data/out/` (после проверки они удаляются). Файл с некорректной структурой создаётся без BOM:
 
```powershell
New-Item data\out\empty.json -ItemType File
New-Item data\out\empty.csv -ItemType File
python -c "open('data/out/bad_items.json','w',encoding='utf-8').write('[1, 2, 3]')"
```
 
**Пустой JSON.**
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/out/empty.json','data/out/x.csv')"
```
 
Результат: `ValueError: Пустой JSON или неподдерживаемая структура`.

![Скриншот 9: пустой JSON](../../images/lab05/image09.png)
 
**Список не из словарей.**
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/out/bad_items.json','data/out/x.csv')"
```
 
Результат: `ValueError: Пустой JSON или неподдерживаемая структура`.

![Скриншот 10: список не из словарей](../../images/lab05/image10.png)
 
**Пустой CSV.**
 
```powershell
python -c "from src.lab05.json_csv import csv_to_json; csv_to_json('data/out/empty.csv','data/out/x.json')"
```
 
Результат: `ValueError: CSV без заголовка или пустой`.

![Скриншот 11: пустой CSV](../../images/lab05/image11.png)
 
**Отсутствующий файл.**
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/samples/net.json','data/out/x.csv')"
```
 
Результат: `FileNotFoundError: [Errno 2] No such file or directory: 'data\\samples\\net.json'`.
 
![Скриншот 12: отсутствующий файл](../../images/lab05/image12.png)
 
**Неверный тип файла.**
 
```powershell
python -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/samples/people.csv','data/out/x.csv')"
```
 
Результат: `ValueError: Неверный тип файла: ожидается .json, получен .csv`.

![Скриншот 13: неверный тип файла](../../images/lab05/image13.png)
 
**Пустой CSV при конвертации в XLSX.**
 
```powershell
python -c "from src.lab05.csv_xlsx import csv_to_xlsx; csv_to_xlsx('data/out/empty.csv','data/out/x.xlsx')"
```
 
Результат: `ValueError: CSV пустой`.
 
![Скриншот 14: пустой CSV при конвертации в XLSX](../../images/lab05/image14.png)
 
После проверки временные файлы удаляются:
 
```powershell
Remove-Item data\out\empty.json, data\out\empty.csv, data\out\bad_items.json
```