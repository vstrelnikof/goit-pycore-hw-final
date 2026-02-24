import logging
from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, Text, TextBox, PopUpDialog, Label, Divider
from cli.tui.forms.base_form import BaseForm
from cli.tui.scene_type import SceneType
from factories.scene_factory import SceneFactory
from models.note import Note

class NoteForm(BaseForm):
    _esc_key_path: str = SceneType.NOTES_GRID

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, can_scroll=False)
    
    def _render_content(self) -> None:
        self._required_fields = ["text"]
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Формат тегів: список через кому"))
        layout.add_widget(Divider())
        layout.add_widget(TextBox(10, label="Текст*:", name="text", as_string=True))
        layout.add_widget(Divider())
        layout.add_widget(Text("Теги:", name="tags"))
        layout.add_widget(Divider())
    
    def reset(self) -> None:
        super().reset()
        self.title = "📝 Нова нотатка" \
            if self._state.edit_index is None else "📝 Редагування нотатки"
        if self._edit_index is not None:
            note: Note = self._state.notes_manager.notes[self._edit_index]
            self.data = {
                "text": note.text,
                "tags": note.tags_string
            }
        else:
            self.data = {
                "text": "", "tags": ""
            }
    
    def _handle_saved(self):
        super().reset()
        SceneFactory.next(SceneType.NOTES_GRID)

    def _ok(self):
        assert self.scene is not None
        self.save()

        if not self.data or not self._validate_form():
            return

        try:
            if self._edit_index is None:
                self._state.notes_manager.add_note(self.data)
            else:
                self._state.notes_manager.edit_note(self._edit_index, self.data)
            self.scene.add_effect(PopUpDialog(self._screen,
                                              "✅ Нотатку успішно збережено!",
                                              ["Чудово"], 
                                              on_close=lambda _: self._handle_saved())
            )
            self._clear_edit()
        except ValueError as e:
            logging.error("Cannot save Note")
            logging.exception(e)
            self.scene.add_effect(
                PopUpDialog(self._screen, f"❌ Помилка: {str(e)}", ["Спробувати ще раз"])
            )
    
    def _cancel(self) -> None:
        self._clear_edit()
        SceneFactory.next(SceneType.NOTES_GRID)

