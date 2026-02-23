from dataclasses import dataclass
from datetime import date, datetime
from typing import final
from uuid import UUID
from helpers.date_helpers import replace_date_year
from models.base_model import BaseModel
from utils.validator import Validator

@final
@dataclass(kw_only=True)
class Contact(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    birthday: str

    @property
    def birthday_date(self) -> (date | None):
        if not self.birthday:
            return None
        contact_birthday: datetime = datetime.strptime(self.birthday, "%Y-%m-%d")
        return contact_birthday.date()

    def _validate(self) -> dict[str, bool]:
        return {
            "name": bool(self.name.strip()),
            "phone": not self.phone or Validator.validate_phone(self.phone),
            "email": not self.email or Validator.validate_email(self.email),
            "birthday": not self.birthday or Validator.validate_date(self.birthday)
        }

    def get_next_birthday_date(self, today: datetime | date = datetime.now().date()) -> (date | None):
        """Повертає дату наступного Дня Народження Контакту"""
        contact_birthday: date | None = self.birthday_date
        if not contact_birthday:
            return None
        this_year_birthday = replace_date_year(contact_birthday, today.year)
        next_birthday = replace_date_year(this_year_birthday, today.year + 1) \
            if this_year_birthday < today else this_year_birthday
        return next_birthday

    def __str__(self):
        return f"{self.name.ljust(15)} | 📱 {self.phone} | 🎂 {self.birthday}"

    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data.get("id"), str):
            data["id"] = UUID(data["id"])
        birthday = data.get("birthday")
        if isinstance(birthday, str):
            data["birthday"] = datetime.strptime(birthday, "%Y-%m-%d") \
            .date().isoformat()
        return cls(**data)
