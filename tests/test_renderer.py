from models.table_row import TableData, TableRow
from cli.classic.renderer import Renderer


def test_format_contacts_table_empty_returns_message() -> None:
    r = Renderer()
    out = r.format_contacts_table([])
    assert "Контакт" in out
    assert "не знайдено" in out


def test_format_contacts_table_one_row_includes_header_and_index() -> None:
    r = Renderer()
    data: TableData = [
        TableRow(cells=["Name", "+380501234567", "a@b.co", "", "1990-01-01"], index=0)
    ]
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


def test_format_note_full_includes_text_and_tags() -> None:
    from models.note import Note

    r = Renderer()
    note = Note(
        text="Повний текст нотатки з кількома словами.", tags=["важливо", "робота"]
    )
    out = r.format_note_full(note)
    assert "Повний текст нотатки" in out
    assert "важливо" in out and "робота" in out
    assert "Теги" in out


def test_format_note_full_without_tags() -> None:
    from models.note import Note

    r = Renderer()
    note = Note(text="Проста нотатка без тегів.")
    out = r.format_note_full(note)
    assert "Проста нотатка без тегів" in out


def test_format_contacts_table_with_total_count_shows_footer() -> None:
    r = Renderer()
    data: TableData = [
        TableRow(cells=["A", "1", "a@b.co", "", "1990-01-01"], index=0),
        TableRow(cells=["B", "2", "b@b.co", "", "1991-01-01"], index=1),
    ]
    out = r.format_contacts_table(data, total_count=10)
    assert "Показано 2 з 10" in out


def test_format_notes_table_with_total_count_shows_footer() -> None:
    r = Renderer()
    data: TableData = [
        TableRow(cells=["Текст", "tag1"], index=0),
    ]
    out = r.format_notes_table(data, total_count=5)
    assert "Показано 1 з 5" in out
