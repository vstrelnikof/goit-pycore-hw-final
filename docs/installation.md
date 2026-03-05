# 📦 Встановлення

## 📋 Потреби

- Python 3.10+
- pip

## 📌 Встановлення як Python-пакет

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

3. **Встановлення пакету (у venv):**

   ```bash
   python -m pip install .
   ```

   Або в режимі розробки (оновлення коду одразу підхоплюються без перевстановлення):

   ```bash
   python -m pip install -e .
   ```

4. **Запуск з будь-якого місця (у межах активованого venv):**

   ```bash
   personal-assistant            # 🖥️ TUI
   personal-assistant --classic  # ⌨️ Класичний режим
   ```

---

## 📌 Запуск без встановлення (варіант «як раніше»)

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

4. **Запуск з кореня проєкту:**

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
