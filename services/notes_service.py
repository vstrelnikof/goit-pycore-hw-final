from typing import final
from decorators.log_command_action import log_command_action
from models.note import Note
from models.table_row import TableData, TableRow
from services.base_service import BaseService
from utils.validator import Validator


@final
class NotesService(BaseService):
    """Сервіс для роботи з нотатками"""

    def find_note_by_id(self, id: str) -> Note | None:
        return next((note for note in self.notes if note.id == id), None)

    @log_command_action()
    def add_note(self, data: dict) -> None:
        new_note: Note = Note.from_dict(data)
        if not new_note.is_valid():
            return
        self.notes.append(new_note)
        self.save()

    @log_command_action()
    def edit_note(self, index: int, data: dict) -> None:
        updated_note: Note = Note.from_dict(data)
        if not updated_note.is_valid():
            return
        self.notes[index] = updated_note
        self.save()

    @log_command_action()
    def delete_note(self, index: int) -> None:
        self.notes.pop(index)
        self.save()

    def get_notes_table_data(
        self, search_term: str, sort_desc: bool = False
    ) -> TableData:
        table_data: TableData = []
        for i, note in enumerate(self.notes):
            is_relevant: bool = Validator.validate_search_term(
                note.text, search_term
            ) or any(
                Validator.validate_search_term(tag, search_term) for tag in note.tags
            )
            if not is_relevant:
                continue
            note_text: str = note.text.replace("\n", " ")
            table_data.append(
                TableRow(
                    cells=[
                        (note_text[:75] + "...") if len(note_text) > 75 else note_text,
                        note.tags_string,
                    ],
                    index=i,
                )
            )
        table_data.sort(
            key=lambda row: self._ukrainian_sort_key(row.cells[1]), reverse=sort_desc
        )
        return table_data

    def save(self) -> None:
        self.storage.save([c.to_dict() for c in self.notes])

    def reload(self) -> None:
        self.notes = [Note.from_dict(n) for n in self.storage.load_list()]
