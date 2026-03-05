from cli.classic.colors import Colors
from cli.classic.forms.base_form import ConsoleFormBase
from utils.validator import Validator


class ContactConsoleForm(ConsoleFormBase):
    """Інтерактивна форма введення / редагування контакту."""

    def _prompt_name(self) -> str:
        existing = self._existing.get("name", "")
        prompt = "👤 Ім'я*: " if not existing else f"👤 Ім'я* [{existing}]: "
        name = self._read_field(prompt, existing)
        while not name:
            print(Colors.error("  ⚠ Поле обов'язкове."))
            name = self._read_field(prompt, existing)
        return name

    def _prompt_phone(self) -> str:
        existing = self._existing.get("phone", "")
        prompt = (
            "📞 Телефон (+380XXXXXXXXX): "
            if not existing
            else f"📞 Телефон (+380XXXXXXXXX) [{existing}]: "
        )
        phone = self._read_field(prompt, existing)
        while phone and not Validator.validate_phone(phone):
            print(Colors.error("  ⚠ Невірний формат. Приклад: +380501234567"))
            phone = self._read_field(prompt, existing)
        return phone

    def _prompt_email(self) -> str:
        existing = self._existing.get("email", "")
        prompt = "✉ Email: " if not existing else f"✉ Email [{existing}]: "
        email = self._read_field(prompt, existing)
        while email and not Validator.validate_email(email):
            print(Colors.error("  ⚠ Невірний формат email."))
            email = self._read_field(prompt, existing)
        return email

    def _prompt_address(self) -> str:
        existing = self._existing.get("address", "")
        prompt = "📍 Адреса: " if not existing else f"📍 Адреса [{existing}]: "
        return self._read_field(prompt, existing)

    def _prompt_birthday(self) -> str:
        raw = self._existing.get("birthday", "")
        if raw and hasattr(raw, "isoformat"):
            existing = raw.isoformat()
        else:
            existing = raw or ""
        prompt = (
            "🎂 День народження (YYYY-MM-DD): "
            if not existing
            else f"🎂 День народження (YYYY-MM-DD) [{existing}]: "
        )
        birthday = self._read_field(prompt, existing)
        while birthday and not Validator.validate_date(birthday):
            print(Colors.error("  ⚠ Невірний формат дати. Приклад: 1990-05-15"))
            birthday = self._read_field(prompt, existing)
        return birthday

    def prompt(self) -> dict:
        self._print_cancel_hint()
        return {
            "name": self._prompt_name(),
            "phone": self._prompt_phone(),
            "email": self._prompt_email(),
            "address": self._prompt_address(),
            "birthday": self._prompt_birthday(),
        }
