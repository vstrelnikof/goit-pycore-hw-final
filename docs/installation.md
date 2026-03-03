# 📦 Встановлення

## 📋 Потреби

- Python 3.10+
- pip

## 📌 Кроки

1. **Клонування репозиторію:**

   ```bash
   git clone https://github.com/vstrelnikof/goit-pycore-hw-final.git
   cd goit-pycore-hw-final
   ```

2. **Створення віртуального середовища та активація:**

   **Windows (cmd):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Встановлення залежностей:**

   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Запуск:**

   - 🖥️ TUI: `python main.py`
   - ⌨️ Класичний режим: `python main.py --classic`

## 🔧 Опційні залежності (розробка)

Для перевірки коду (ruff) та тестів:

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests/ -v
```

Детальніше — [development.md](development.md).
