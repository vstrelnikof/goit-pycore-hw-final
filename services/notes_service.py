from typing import final
from decorators.log_decorator import log_action
from models.note import Note
from services.base_service import BaseService

@final
class NotesService(BaseService):
    notes: list[Note]

    def find_note_by_id(self, id: str) -> (Note | None):
        return next((note for note in self.notes if note.id == id), None)

    @log_action
    def add_note(self, data: dict) -> None:
        new_note: Note = Note.from_dict(data)
        if not new_note.is_valid():
            return
        self.notes.append(new_note)
        self.save()
    
    @log_action
    def edit_note(self, index: int, data: dict) -> None:
        updated_note: Note = Note.from_dict(data)
        if not updated_note.is_valid():
            return
        self.notes[index] = updated_note
        self.save()

    @log_action
    def delete_note(self, index: int) -> None:
        self.notes.pop(index)
        self.save()
    
    def get_notes_table_data(self, search_term: str, sort_desc: bool = False) -> list:
        table_data: list[tuple[list[str], int]] = []
        for i, note in enumerate(self.notes):
            is_relevant: bool = search_term in note.text.lower() or \
                any([tag for tag in note.tags if search_term in tag.lower()])
            if not is_relevant:
                continue
            note_text: str = note.text.replace('\n', ' ')
            table_row: tuple[list[str], int] = ([(note_text[:60] + '...')
                if len(note_text) > 60 else note_text,
                note.tags_string], i)
            table_data.append(table_row)
        table_data.sort(key=lambda row: row[1], reverse=sort_desc)
        return table_data

    def save(self) -> None:
        self.storage.save([c.to_dict() for c in self.notes])
    
    def reload(self) -> None:
        self.notes = [Note.from_dict(n) for n in self.storage.load()]
