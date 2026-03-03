import re
from typing import final


@final
class Validator:
    """Утилітний клас, містить різноманітні методи валідації"""

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return re.match(r"^\+380\d{9}$", phone) is not None

    @staticmethod
    def validate_email(email: str) -> bool:
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

    @staticmethod
    def validate_date(date_str: str) -> bool:
        return re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", date_str) is not None

    @staticmethod
    def validate_days(days_str: str) -> bool:
        return days_str.isdigit()
