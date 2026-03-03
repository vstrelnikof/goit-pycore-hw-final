import logging
from typing import TYPE_CHECKING

from faker import Faker

if TYPE_CHECKING:
    from utils.state import AppState

logger = logging.getLogger(__name__)

_FAKER = Faker("uk_UA")

# Теми для нотаток і тегів — реалістичний контент для скріншотів
_NOTE_TEMPLATES = [
    "Замовити квитки на концерт на наступний тиждень.",
    "Передзвонити стоматологу щодо запису.",
    "Купити подарунок на день народження Маші.",
    "Перевірити баланс комунальних платежів.",
    "Підготувати презентацію до п'ятниці.",
    "Забрати посилку з відділення Нової пошти.",
    "Записатися на курси англійської.",
    "Роздрукувати документи до податкової.",
    "Зустріч з командою о 15:00 — підсумки спринту.",
    "Рецепт борщу від бабусі — зберегти.",
    "Пароль від Wi-Fi офісу: записати в безпечне місце.",
    "Ідеї для відпустки: Карпати або Одеса.",
    "Список продуктів на тиждень — скласти в суботу.",
    "Нагадування: оплатити страховку авто до кінця місяця.",
    "Книги до прочитання: «Кобзар», «Тіні забутих предків».",
]
_NOTE_TAGS = [
    "робота",
    "особисте",
    "покупки",
    "здоров'я",
    "події",
    "ідеї",
    "паролі",
    "подорожі",
    "нагадування",
    "читання",
]


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
    text = _FAKER.random_element(_NOTE_TEMPLATES)
    tags = _FAKER.random_elements(
        elements=_NOTE_TAGS, length=_FAKER.random_int(1, 4), unique=True
    )
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
