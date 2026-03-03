# ⚙️ Конфігурація

Налаштування застосунку задаються файлом **config.yaml** та (опційно) аргументами командного рядка. Аргументи мають пріоритет над значеннями з файлу.

## 📄 config.yaml

Файл у корені проєкту. Приклад:

```yaml
app:
  log_level: 20          # 10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL
  theme: "default"       # default / monochrome / green / bright (TUI)
  classic: false        # true — запуск у класичному консольному режимі
  app_data_paths:
    address_book: data/contacts.json
    notes: data/notes.json
```

- **log_level** — рівень логування у файл `assistant.log`.
- **theme** — тема asciimatics (враховується лише в TUI).
- **classic** — якщо `true`, при запуску без `--classic` все одно використовується класичний режим.
- **app_data_paths** — шляхи до JSON-файлів контактів та нотаток (відносно поточної робочої директорії).

## 🔧 Аргументи командного рядка

| Аргумент | Опис | Приклад |
|----------|------|---------|
| `--theme` | Тема TUI | `--theme green` |
| `--log-level` | Рівень логування | `--log-level 10` |
| `--classic` | Увімкнути класичний режим | `--classic` |

Приклад:

```bash
python main.py --classic --log-level 10
```

Якщо аргумент не передано, використовується значення з config.yaml або значення за замовчуванням.

## ⚠️ Відсутність config.yaml

Якщо файл відсутній або пошкоджений, застосунок стартує з налаштуваннями за замовчуванням (зокрема `classic: false`, стандартні шляхи до `data/contacts.json` та `data/notes.json`).
