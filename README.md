# **Лабораторные работы по программированию на Python**
 
</div>

## Навигация
 
| № | Тема | Что отработано | Код |
|:-:|---|---|---|
| **ЛР1** | Ввод/вывод и форматирование | `input`, `print`, f-строки, циклы | [`src/lab01`](src/lab01) |
| **ЛР2** | Коллекции и матрицы | `list`, `tuple`, `set`, `dict`, 2D-списки | [`src/lab02`](src/lab02) |
| **ЛР3** | Тексты и частоты слов | нормализация, регулярные выражения, словари | [`src/lab03`](src/lab03), [`src/lib/text.py`](src/lib/text.py) |
| **ЛР4** | Файлы TXT/CSV | `pathlib`, кодировки, `csv`, `argparse` | [`src/lab04`](src/lab04) |
| **ЛР5** | JSON и конвертации | `json`, `DictReader`/`DictWriter`, `openpyxl` | [`src/lab05`](src/lab05) |
| **ЛР6** | CLI‑утилиты с argparse | `argparse`, `pathlib`, `sys` | [`src/lab06`](src/lab06) |
| **ЛР7** | Поиск, сортировка и измерение времени | `random`, `timeit`, `pandas`, `matplotlib.pyplot` | [`src/lab07`](src/lab07) |
 
## Структура репозитория
 
```text
python_labs/
├─ README.md
├─ requirements.txt        # openpyxl (ЛР5)
├─ src/
│  ├─ lib/text.py          # переиспользуемый модуль (ЛР3)
│  ├─ lab01 … lab07/       # решения по лабораторным
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
