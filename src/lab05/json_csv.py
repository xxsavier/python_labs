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