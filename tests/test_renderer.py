from models.table_row import TableData, TableRow
from cli.classic.renderer import Renderer

def test_format_contacts_table_empty_returns_message() -> None:
    r = Renderer()
    out = r.format_contacts_table([])
    assert "Контакт" in out
    assert "не знайдено" in out

def test_format_contacts_table_one_row_includes_header_and_index() -> None:
    r = Renderer()
    data: TableData = [TableRow(cells=["Name", "+380501234567", "a@b.co", "", "1990-01-01"], index=0)]
    out = r.format_contacts_table(data)
    assert "Ім'я" in out or "Name" in out
    assert "0" in out
    assert "Name" in out

def test_format_notes_table_empty_returns_message() -> None:
    r = Renderer()
    out = r.format_notes_table([])
    assert "Нотаток" in out
    assert "не знайдено" in out

def test_format_birthdays_table_empty_returns_message() -> None:
    r = Renderer()
    out = r.format_birthdays_table([])
    assert "іменинників" in out or "період" in out
