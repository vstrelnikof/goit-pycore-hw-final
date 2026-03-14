from pathlib import Path
import pytest
from models.contact import Contact
from providers.storage_provider import StorageProvider
from services.address_book_service import AddressBookService
from services.notes_service import NotesService


@pytest.fixture
def address_book_service(tmp_path: Path) -> AddressBookService:
    storage = StorageProvider(tmp_path / "contacts.json")
    service = AddressBookService(storage)
    # Гарантуємо, що список контактів порожній
    service.contacts.clear()
    return service


@pytest.fixture
def notes_service(tmp_path: Path) -> NotesService:
    storage = StorageProvider(tmp_path / "notes.json")
    service = NotesService(storage)
    service.notes.clear()
    return service


def test_add_contact_valid_creates_and_persists_record(
    address_book_service: AddressBookService,
) -> None:
    data = {
        "name": "John Doe",
        "phone": "+380501234567",
        "email": "john@example.com",
        "address": "Kyiv",
        "birthday": "1990-01-01",
    }

    address_book_service.add_contact(data)

    assert len(address_book_service.contacts) == 1
    stored = list(address_book_service.storage.load_list())
    assert len(stored) == 1
    assert stored[0]["name"] == "John Doe"


def test_add_contact_invalid_does_not_save(
    address_book_service: AddressBookService,
) -> None:
    # Некоректне ім'я робить модель невалідною
    data = {
        "name": "   ",
        "phone": "12345",
        "email": "not-an-email",
        "address": "",
        "birthday": "",
    }

    address_book_service.add_contact(data)

    assert len(address_book_service.contacts) == 0
    assert list(address_book_service.storage.load_list()) == []


def test_edit_and_delete_contact_update_storage(
    address_book_service: AddressBookService,
) -> None:
    address_book_service.add_contact(
        {
            "name": "Old Name",
            "phone": "+380501234567",
            "email": "old@example.com",
            "address": "Old address",
            "birthday": "1990-01-01",
        }
    )
    assert len(address_book_service.contacts) == 1

    contact_id = str(address_book_service.contacts[0].id)
    address_book_service.edit_contact(
        contact_id,
        {
            "name": "New Name",
            "phone": "+380501234567",
            "email": "new@example.com",
            "address": "New address",
            "birthday": "1990-01-01",
        },
    )

    assert address_book_service.contacts[0].name == "New Name"

    stored_after_edit = list(address_book_service.storage.load_list())
    assert stored_after_edit[0]["name"] == "New Name"

    contact_id = str(address_book_service.contacts[0].id)
    address_book_service.delete_contact(contact_id)

    assert len(address_book_service.contacts) == 0
    assert list(address_book_service.storage.load_list()) == []


def test_get_contacts_table_data_filters_by_search_term(
    address_book_service: AddressBookService,
) -> None:
    # Створюємо контакти напряму, щоб не залежати від валідації у цьому тесті
    address_book_service.contacts = [
        Contact(
            name="Alice",
            phone="+380501234567",
            email="alice@example.com",
            address="Kyiv",
            birthday="1990-01-01",
        ),
        Contact(
            name="Bob",
            phone="+380671234567",
            email="bob@example.com",
            address="Lviv",
            birthday="1992-02-02",
        ),
    ]

    rows = address_book_service.get_contacts_table_data("alice")
    assert len(rows) == 1
    assert rows[0].cells[0] == "Alice"

    # Wildcard * — будь-які символи
    rows_wild = address_book_service.get_contacts_table_data("*ice")
    assert len(rows_wild) == 1
    assert rows_wild[0].cells[0] == "Alice"
    rows_wild = address_book_service.get_contacts_table_data("Ali*")
    assert len(rows_wild) == 1
    assert rows_wild[0].cells[0] == "Alice"


def test_add_note_valid_creates_and_persists_record(
    notes_service: NotesService,
) -> None:
    notes_service.add_note({"text": "Test note", "tags": "one, two"})

    assert len(notes_service.notes) == 1
    stored = list(notes_service.storage.load_list())
    assert len(stored) == 1
    assert stored[0]["text"] == "Test note"
    # Теги зберігаються як список
    assert stored[0]["tags"] == ["one", "two"]


def test_add_note_invalid_does_not_save(notes_service: NotesService) -> None:
    # Порожній текст робить нотатку невалідною
    notes_service.add_note({"text": "   ", "tags": ""})

    assert len(notes_service.notes) == 0
    assert list(notes_service.storage.load_list()) == []


def test_get_notes_table_data_filters_and_sorts(
    notes_service: NotesService,
) -> None:
    notes_service.add_note({"text": "First note text", "tags": "one"})
    notes_service.add_note({"text": "Second important", "tags": "two"})

    # Пошук за текстом (регістр ігнорується завдяки lower())
    rows = notes_service.get_notes_table_data("second")
    assert len(rows) == 1
    assert "Second important" in rows[0].cells[0]

    # Wildcard * у пошуку
    rows_wild = notes_service.get_notes_table_data("*ond*")
    assert len(rows_wild) == 1
    assert "Second important" in rows_wild[0].cells[0]

    # Без фільтру, але з сортуванням за тегами спаданням
    all_rows_desc = notes_service.get_notes_table_data("", sort_desc=True)
    assert len(all_rows_desc) == 2
    assert all_rows_desc[0].cells[1] >= all_rows_desc[1].cells[1]
