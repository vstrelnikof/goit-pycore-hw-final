# 🧪 Розробка та тести

## 🔒 Git-хуки (pre-commit)

У проєкті налаштовані Git-хуки: перевірки запускаються автоматично перед **commit** і перед **push**. Це гарантує, що в репозиторій не потраплять код без проходження лінтера та тестів.

### Встановлення хуків (один раз після клонування)

1. Встановіть dev-залежності (у тому числі `pre-commit`):
   ```bash
   python -m pip install -r requirements-dev.txt
   ```
2. Встановіть хуки та оновіть ревізії в `.pre-commit-config.yaml` (скрипт виконує `autoupdate` + `install`):
   ```bash
   # Windows (PowerShell):
   .\scripts\setup-hooks.ps1

   # Linux / macOS:
   bash scripts/setup-hooks.sh
   ```
   Або вручну:
   ```bash
   python -m pre-commit autoupdate
   python -m pre-commit install
   python -m pre-commit install --hook-type pre-push
   ```

Після цього:

- **Перед кожним commit** запускаються **ruff check** та **ruff format** (код перевіряється і при потребі автоматично форматується).
- **Перед кожним push** запускаються **усі тести** (`pytest tests/`). Якщо хоч один тест падає, **push блокується** — запушити зміни можна лише коли усі тести зелені.

### Ручний запуск перевірок як у хуках

```bash
python -m pre-commit run --all-files                        # усі хуки (pre-commit стадія)
python -m pre-commit run --all-files --hook-stage pre-push  # лише тести (як перед push)
```

### Пропуск хуків (не рекомендується)

У виняткових випадках можна обійти перевірки:

- При commit: `git commit --no-verify`
- При push: `git push --no-verify`

Користуйтеся цим лише якщо розумієте наслідки; у звичайному workflow хуки мають залишатися увімкненими.

### Якщо pre-commit падає (Windows / помилки ruff або pytest)

- **Запускай команди з кореня проєкту з активованим venv** (наприклад ` .venv\Scripts\activate` у PowerShell), щоб `python` і пакети були з середовища проєкту.
- Перший запуск `pre-commit run --all-files` може завантажити середовище для ruff — це нормально.
- Якщо падає хук **pytest**: переконайся, що в тому ж терміналі проходять команди  
  `python -m pytest tests/ -v` та `python -m ruff check .`. Якщо так — запускай pre-commit з цього ж терміналу (з активованим venv).

---

## ✅ Тести

Запуск усіх тестів:

```bash
python -m pytest tests/ -v
```

Короткий вивід:

```bash
python -m pytest tests/ --tb=short
```

Тести покривають: завантаження конфігурації (у т.ч. `--classic` і `classic` у файлі), моделі (BaseModel, Note), провайдер сховища, TableRow/TableData, CommandDispatcher (парсинг, підказки, виконання команд), Renderer (порожні таблиці та таблиці з даними), Validator, AppState, AddressBookService, NotesService та helpers (date_helpers).

## 🔍 Лінтер та форматування

Опційно встановіть dev-залежності:

```bash
python -m pip install -r requirements-dev.txt
```

Перевірка коду (ruff):

```bash
python -m ruff check .
python -m ruff format . --check
```

Автоформатування:

```bash
python -m ruff format .
python -m ruff check . --fix
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
