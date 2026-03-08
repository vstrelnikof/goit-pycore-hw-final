import logging
import random
from typing import TYPE_CHECKING

from faker import Faker

if TYPE_CHECKING:
    from utils.state import AppState

logger = logging.getLogger(__name__)

_FAKER = Faker("uk_UA")


def _random_note_text() -> str:
    """Повертає багаторядковий випадковий текст без шаблонів."""
    num_paragraphs = random.randint(1, 5)
    paragraphs = _FAKER.paragraphs(nb=num_paragraphs)
    return "\n\n".join(paragraphs)


def _random_tags(max_tags: int = 20) -> list[str]:
    """Повертає список унікальних випадкових слів (тегів), від 1 до max_tags."""
    count = random.randint(1, max_tags)
    seen: set[str] = set()
    while len(seen) < count:
        seen.add(_FAKER.word())
    return list(seen)


def _generate_contact_data() -> dict:
    """Повертає словник для Contact.from_dict (валідний телефон +380XXXXXXXXX)."""
    birth = _FAKER.date_of_birth(minimum_age=18, maximum_age=80)
    return {
        "name": _FAKER.name(),
        "phone": _FAKER.numerify(text="+380%%%%%%%%%"),
        "email": _FAKER.ascii_safe_email(),
        "address": _FAKER.address().replace("\n", ", "),
        "birthday": birth.strftime("%Y-%m-%d"),
    }


def _generate_note_data() -> dict:
    """Повертає словник для Note.from_dict (text + tags)."""
    text = _random_note_text()
    tags = _random_tags(max_tags=20)
    return {"text": text, "tags": tags}


def create_fakes(
    state: "AppState",
    contacts_count: int = 0,
    notes_count: int = 0,
) -> None:
    """Додає фейкові контакти та нотатки до поточного стану (сервіси самі зберігають)."""
    if contacts_count <= 0 and notes_count <= 0:
        return
    if contacts_count > 0:
        for _ in range(contacts_count):
            data = _generate_contact_data()
            state.address_book_manager.add_contact(data)
        logger.info("Created %s fake contacts", contacts_count)
    if notes_count > 0:
        for _ in range(notes_count):
            data = _generate_note_data()
            # NotesService.add_note очікує dict; tags можуть бути list (from_dict перетворить)
            state.notes_manager.add_note(data)
        logger.info("Created %s fake notes", notes_count)
