# 📒 Персональний помічник

Консольний застосунок для керування контактами та нотатками: два режими інтерфейсу (TUI на asciimatics і класичний консольний), збереження даних у JSON, валідація полів і підказки команд.

## 🖥️ Режими роботи

| Режим | Запуск | Опис |
|-------|--------|------|
| **🖥️ TUI** | `python main.py` або `personal-assistant` | Інтерактивний інтерфейс (asciimatics): дешборд, форми, таблиці. |
| **⌨️ Classic** | `python main.py --classic` або `personal-assistant --classic`, або `classic: true` у config | Консольний цикл: команди вводяться з клавіатури, вивід у консоль з кольорами. |

Детально про кожен режим — у розділах [TUI](docs/tui.md) та [Classic](docs/classic.md).

## 🚀 Швидкий старт

### Встановлення як Python-пакет (рекомендовано)

```bash
git clone https://github.com/vstrelnikof/goit-pycore-hw-final.git
cd goit-pycore-hw-final
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
python -m pip install .
```

Після цього застосунок доступний як команда з будь-якого місця (у межах активованого venv):

```bash
personal-assistant            # TUI
personal-assistant --classic  # класичний режим
```

### Запуск без встановлення (старий варіант)

```bash
git clone https://github.com/vstrelnikof/goit-pycore-hw-final.git
cd goit-pycore-hw-final
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Для класичного режиму:

```bash
python main.py --classic
```

Повна інструкція з встановлення — [docs/installation.md](docs/installation.md).

## ✨ Функціональність

- **📇 Контакти**: додавання, пошук, редагування, видалення; поля: ім'я, телефон (+380...), email, адреса, день народження; валідація та список днів народження на N днів.
- **📝 Нотатки**: текст і теги; пошук за текстом/тегами; сортування за тегами; CRUD.
- **💾 Збереження**: контакти — `data/contacts.json`, нотатки — `data/notes.json` (шляхи налаштовуються в [config.yaml](config.yaml)).

## ⚙️ Конфігурація

Файл [config.yaml](config.yaml) та аргументи CLI (`--theme`, `--log-level`, `--classic`). Детально — [docs/configuration.md](docs/configuration.md).

## 📚 Документація

- 📦 [Встановлення](docs/installation.md)
- 🖥️ [TUI (інтерфейс asciimatics)](docs/tui.md)
- ⌨️ [Classic (консольний режим)](docs/classic.md)
- ⚙️ [Конфігурація](docs/configuration.md)
- 🧪 [Розробка та тести](docs/development.md)