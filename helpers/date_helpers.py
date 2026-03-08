from datetime import date, timedelta


def replace_date_year(d: date, year: int) -> date:
    """Функція яка змінює рік в даті, враховуючи високосний"""
    try:
        return d.replace(year=year)
    except ValueError:
        return d.replace(year=year, month=2, day=28)


def days_left_in_year() -> int:
    """Кількість днів до кінця року"""
    today: date = date.today()
    end_of_year: date = date(today.year, 12, 31)
    difference: timedelta = end_of_year - today
    return difference.days
