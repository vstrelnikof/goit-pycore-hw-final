# 🧪 Розробка та тести

## 🔒 Git-хуки (pre-commit)

У проєкті налаштовані Git-хуки: перевірки запускаються автоматично перед **commit** і перед **push**. Це гарантує, що в репозиторій не потраплять код без проходження лінтера та тестів.

### Встановлення хуків (один раз після клонування)

1. Встановіть dev-залежності (у тому числі `pre-commit`):
   ```bash
   python -m pip install -r requirements-dev.txt
   ```
2. Встановіть хуки в репозиторії:
   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

Після цього:

- **Перед кожним commit** запускаються **ruff check** та **ruff format** (код перевіряється і при потребі автоматично форматується).
- **Перед кожним push** запускаються **усі тести** (`pytest tests/`). Якщо хоч один тест падає, **push блокується** — запушити зміни можна лише коли усі тести зелені.

### Ручний запуск перевірок як у хуках

```bash
pre-commit run --all-files                     # усі хуки (commit-стадія)
pre-commit run --all-files --hook-stage push   # лише тести (як перед push)
```

### Пропуск хуків (не рекомендується)

У виняткових випадках можна обійти перевірки:

- При commit: `git commit --no-verify`
- При push: `git push --no-verify`

Користуйтеся цим лише якщо розумієте наслідки; у звичайному workflow хуки мають залишатися увімкненими.

---

## ✅ Тести

Запуск усіх тестів:

```bash
pytest tests/ -v
```

Короткий вивід:

```bash
pytest tests/ --tb=short
```

Тести покривають: завантаження конфігурації (у т.ч. `--classic` і `classic` у файлі), моделі (BaseModel, Note), провайдер сховища, TableRow/TableData, CommandDispatcher (парсинг, підказки, виконання команд), Renderer (порожні таблиці та таблиці з даними), Validator, AppState, AddressBookService, NotesService та helpers (date_helpers).

## 🔍 Лінтер та форматування

Опційно встановіть dev-залежності:

```bash
python -m pip install -r requirements-dev.txt
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
