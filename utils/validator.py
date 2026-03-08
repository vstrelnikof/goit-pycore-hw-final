import re
from typing import final


@final
class Validator:
    """Утилітний клас, містить різноманітні методи валідації"""

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Accepts E.164 format: + followed by 7–15 digits (country code + number)."""
        return re.match(r"^\+[1-9]\d{6,14}$", phone) is not None

    @staticmethod
    def validate_email(email: str) -> bool:
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

    @staticmethod
    def validate_date(date_str: str) -> bool:
        return re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", date_str) is not None

    @staticmethod
    def validate_days(days_str: str) -> bool:
        return days_str.isdigit()

    @staticmethod
    def validate_search_term(text: str, search_term: str, wildcard: str = "*") -> bool:
        if not search_term:
            return True
        text_lower = text.lower()
        search_lower = search_term.lower()
        if wildcard not in search_lower:
            return search_lower in text_lower
        escaped = re.escape(wildcard)
        parts = re.split(rf"{escaped}+", search_lower)
        pattern = ".*".join(re.escape(p) for p in parts if p)
        if not pattern:
            return True
        return re.search(pattern, text_lower) is not None
