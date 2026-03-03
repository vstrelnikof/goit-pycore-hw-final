from cli.classic.colors import Colors
from utils.validator import Validator


class ContactConsoleForm:
    """Інтерактивна форма введення / редагування контакту."""

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def prompt(self) -> dict:
        data: dict = {}

        # Ім'я
        existing_name = self._existing.get("name", "")
        name_prompt = (
            "👤 Ім'я*: " if not existing_name else f"👤 Ім'я* [{existing_name}]: "
        )
        name = input(Colors.accent(name_prompt)).strip() or existing_name
        while not name:
            print(Colors.error("  ⚠ Поле обов'язкове."))
            name = input(Colors.accent(name_prompt)).strip() or existing_name
        data["name"] = name

        # Телефон
        existing_phone = self._existing.get("phone", "")
        phone_prompt = (
            "📞 Телефон (+380XXXXXXXXX): "
            if not existing_phone
            else f"📞 Телефон (+380XXXXXXXXX) [{existing_phone}]: "
        )
        phone = input(Colors.accent(phone_prompt)).strip() or existing_phone
        while phone and not Validator.validate_phone(phone):
            print(Colors.error("  ⚠ Невірний формат. Приклад: +380501234567"))
            phone = input(Colors.accent(phone_prompt)).strip() or existing_phone
        data["phone"] = phone

        # Email
        existing_email = self._existing.get("email", "")
        email_prompt = (
            "✉ Email: " if not existing_email else f"✉ Email [{existing_email}]: "
        )
        email = input(Colors.accent(email_prompt)).strip() or existing_email
        while email and not Validator.validate_email(email):
            print(Colors.error("  ⚠ Невірний формат email."))
            email = input(Colors.accent(email_prompt)).strip() or existing_email
        data["email"] = email

        # Адреса
        existing_address = self._existing.get("address", "")
        address_prompt = (
            "📍 Адреса: "
            if not existing_address
            else f"📍 Адреса [{existing_address}]: "
        )
        data["address"] = (
            input(Colors.accent(address_prompt)).strip() or existing_address
        )

        # День народження
        existing_birthday_raw = self._existing.get("birthday", "")
        if existing_birthday_raw and hasattr(existing_birthday_raw, "isoformat"):
            existing_birthday = existing_birthday_raw.isoformat()
        else:
            existing_birthday = existing_birthday_raw or ""
        birthday_prompt = (
            "🎂 День народження (YYYY-MM-DD): "
            if not existing_birthday
            else f"🎂 День народження (YYYY-MM-DD) [{existing_birthday}]: "
        )
        birthday = input(Colors.accent(birthday_prompt)).strip() or existing_birthday
        while birthday and not Validator.validate_date(birthday):
            print(Colors.error("  ⚠ Невірний формат дати. Приклад: 1990-05-15"))
            birthday = (
                input(Colors.accent(birthday_prompt)).strip() or existing_birthday
            )
        data["birthday"] = birthday

        return data
