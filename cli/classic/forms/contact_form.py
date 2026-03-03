from utils.validator import Validator

class ContactConsoleForm:
    """Інтерактивна форма введення / редагування контакту."""

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def prompt(self) -> dict:
        data: dict = {}

        name = input("Ім'я*: ").strip() or self._existing.get("name", "")
        while not name:
            print("  Поле обов'язкове.")
            name = input("Ім'я*: ").strip() or self._existing.get("name", "")
        data["name"] = name

        phone = input("Телефон (+380XXXXXXXXX): ").strip() or self._existing.get("phone", "")
        while phone and not Validator.validate_phone(phone):
            print("  Невірний формат. Приклад: +380501234567")
            phone = input("Телефон: ").strip() or self._existing.get("phone", "")
        data["phone"] = phone

        email = input("Email: ").strip() or self._existing.get("email", "")
        while email and not Validator.validate_email(email):
            print("  Невірний формат email.")
            email = input("Email: ").strip() or self._existing.get("email", "")
        data["email"] = email

        data["address"] = input("Адреса: ").strip() or self._existing.get("address", "")

        birthday = input("День народження (YYYY-MM-DD): ").strip() or self._existing.get("birthday", "")
        if self._existing.get("birthday") and hasattr(self._existing["birthday"], "isoformat"):
            birthday = birthday or self._existing["birthday"].isoformat()
        while birthday and not Validator.validate_date(birthday):
            print("  Невірний формат дати. Приклад: 1990-05-15")
            birthday = input("День народження: ").strip() or self._existing.get("birthday", "")
        data["birthday"] = birthday

        return data
