from enum import StrEnum
from typing import final

@final
class SceneType(StrEnum):
    """Типи сцен. Використовуються як унікальне ім'я для сцени."""
    MAIN = "Main"
    CONTACT_FORM = "ContactForm"
    CONTACTS_GRID = "ContactsList"
    NOTE_FORM = "NoteForm"
    NOTES_GRID = "NotesList"
    BIRTHDAYS_GRID  = "BirthDaysList"