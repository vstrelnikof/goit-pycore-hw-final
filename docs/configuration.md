# ⚙️ Конфігурація

Налаштування застосунку задаються файлом(ами) **config.yaml** / **config.\<profile\>.yaml** та (опційно) аргументами командного рядка. Аргументи мають пріоритет над значеннями з файлу.

## 📄 config.yaml

Базовий файл конфігурації — `config.yaml` у корені проєкту. Приклад:

```yaml
app:
  log_level: 20          # 10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL
  theme: "default"       # default / monochrome / green / bright (TUI)
  classic: false         # true — запуск у класичному консольному режимі
  app_data_paths:
    address_book: data/contacts.json
    notes: data/notes.json
```

- **log_level** — рівень логування у файл `assistant.log`.
- **theme** — тема asciimatics (враховується лише в TUI).
- **classic** — якщо `true`, при запуску без `--classic` все одно використовується класичний режим.
- **app_data_paths** — шляхи до JSON-файлів контактів та нотаток (відносно поточної робочої директорії).

Також можна створювати кілька конфігів для різних сценаріїв (профілів), наприклад:

- `config.dev.yaml`
- `config.classic.yaml`
- `config.demo.yaml`

Профіль обирається через аргумент `--config` (див. нижче).

## 🔧 Аргументи командного рядка

| Аргумент | Опис | Приклад |
|----------|------|---------|
| `--theme` | Тема TUI | `--theme green` |
| `--log-level` | Рівень логування | `--log-level <number>` |
| `--classic` | Увімкнути класичний режим | `--classic` |
| `--create-fakes-contacts` | Згенерувати N фейкових контактів (uk_UA) перед стартом | `--create-fakes-contacts <number>` |
| `--create-fakes-notes` | Згенерувати N фейкових нотаток (uk_UA) перед стартом | `--create-fakes-notes <number>` |
| `--config` | Вибір конфіг-файлу або профілю | `--config dev` / `--config path/to/config.custom.yaml` |

Приклади запуску:

```bash
python main.py --classic --log-level 10
```

Запуск з попередньою генерацією тестових даних:

```bash
python main.py --create-fakes-contacts <number> --create-fakes-notes <number>
```

Запуск із різними конфігами:

```bash
# Використати профіль config.dev.yaml
python main.py --config dev

# Використати явний шлях до файлу конфігурації
python main.py --config ./configs/presentation.yaml
```

Якщо аргумент не передано, використовується значення з config.yaml або значення за замовчуванням.

## ⚠️ Відсутність config.yaml

Якщо файл відсутній або пошкоджений, застосунок стартує з налаштуваннями за замовчуванням (зокрема `classic: false`, стандартні шляхи до `data/contacts.json` та `data/notes.json`).
