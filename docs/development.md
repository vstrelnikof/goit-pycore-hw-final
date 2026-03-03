# 🧪 Розробка та тести

## ✅ Тести

Запуск усіх тестів:

```bash
pytest tests/ -v
```

Короткий вивід:

```bash
pytest tests/ --tb=short
```

Тести покривають: завантаження конфігурації (у т.ч. `--classic` і `classic` у файлі), моделі (BaseModel, Note), провайдер сховища, TableRow/TableData, CommandDispatcher (парсинг, підказки, виконання команд), Renderer (порожні таблиці та таблиці з даними).

## 🔍 Лінтер та форматування

Опційно встановіть dev-залежності:

```bash
pip install -r requirements-dev.txt
```

Перевірка коду (ruff):

```bash
ruff check .
ruff format . --check
```

Автоформатування:

```bash
ruff format .
ruff check . --fix
```

## 📁 Структура проєкту (коротко)

- **main.py** — точка входу; вибір TUI або classic за конфігом.
- **models/** — моделі даних (Contact, Note, AppConfig, TableRow тощо).
- **services/** — бізнес-логіка (AddressBookService, NotesService).
- **providers/** — конфіг та сховище (ConfigProvider, StorageProvider).
- **cli/tui/** — asciimatics: сцени, форми, таблиці.
- **cli/classic/** — класичний режим: dispatcher, renderer, форми, кольори.
- **tests/** — pytest-тести.

## 📐 Типізація

У проєкті використовуються type hints (аннотації). Для табличних даних замість «сирих» `list[tuple[list[str], int]]` використовуються типи **TableRow** та **TableData** з [models/table_row.py](../models/table_row.py).
