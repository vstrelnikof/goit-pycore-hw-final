from datetime import date
import helpers.date_helpers as dh
from helpers.date_helpers import days_left_in_year, replace_date_year

def test_replace_date_year_keeps_month_and_day_for_regular_dates() -> None:
    original = date(2020, 5, 10)
    result = replace_date_year(original, 2025)
    assert result == date(2025, 5, 10)

def test_replace_date_year_handles_leap_day_to_non_leap_year() -> None:
    original = date(2020, 2, 29)
    # 2021 не високосний, очікуємо 28 лютого
    result = replace_date_year(original, 2021)
    assert result == date(2021, 2, 28)

def test_days_left_in_year_uses_today(monkeypatch) -> None:
    class FixedDate(date):
        @classmethod
        def today(cls):  # type: ignore[override]
            # Фіксуємо дату 30 грудня невисокосного року
            return cls(2025, 12, 30)

    monkeypatch.setattr(dh, "date", FixedDate)

    # До кінця року лишається 1 день (31 грудня)
    assert days_left_in_year() == 1

