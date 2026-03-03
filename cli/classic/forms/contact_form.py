from cli.classic.colors import Colors
from utils.validator import Validator


class ContactConsoleForm:
    """Інтерактивна форма введення / редагування контакту."""

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def prompt(self) -> dict:
        data: dict = {}

        name = input(Colors.accent("👤 Ім'я*: ")).strip() or self._existing.get("name", "")
        while not name:
            print(Colors.error("  ⚠ Поле обов'язкове."))
            name = input(Colors.accent("👤 Ім'я*: ")).strip() or self._existing.get("name", "")
        data["name"] = name

        phone = input(Colors.accent("📞 Телефон (+380XXXXXXXXX): ")).strip() or self._existing.get("phone", "")
        while phone and not Validator.validate_phone(phone):
            print(Colors.error("  ⚠ Невірний формат. Приклад: +380501234567"))
            phone = input(Colors.accent("📞 Телефон: ")).strip() or self._existing.get("phone", "")
        data["phone"] = phone

        email = input(Colors.accent("✉ Email: ")).strip() or self._existing.get("email", "")
        while email and not Validator.validate_email(email):
            print(Colors.error("  ⚠ Невірний формат email."))
            email = input(Colors.accent("✉ Email: ")).strip() or self._existing.get("email", "")
        data["email"] = email

        data["address"] = input(Colors.accent("📍 Адреса: ")).strip() or self._existing.get("address", "")

        birthday = input(Colors.accent("🎂 День народження (YYYY-MM-DD): ")).strip() or self._existing.get("birthday", "")
        if self._existing.get("birthday") and hasattr(self._existing["birthday"], "isoformat"):
            birthday = birthday or self._existing["birthday"].isoformat()
        while birthday and not Validator.validate_date(birthday):
            print(Colors.error("  ⚠ Невірний формат дати. Приклад: 1990-05-15"))
            birthday = input(Colors.accent("🎂 День народження: ")).strip() or self._existing.get("birthday", "")
        data["birthday"] = birthday

        return data
