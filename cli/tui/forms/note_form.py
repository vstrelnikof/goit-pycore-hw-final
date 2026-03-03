import logging
from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, Text, TextBox, PopUpDialog, Label, Divider
from cli.tui.forms.base_form import BaseForm
from enums.scene_type import SceneType
from factories.scene_factory import SceneFactory
from models.note import Note

logger = logging.getLogger(__name__)


class NoteForm(BaseForm):
    """Клас форми створення/редагування нататки"""

    @property
    def _esc_key_path(self) -> SceneType:
        return SceneType.NOTES_GRID

    @property
    def _required_fields(self) -> list[str]:
        return ["text"]

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, can_scroll=False)

    def _render_content(self) -> None:
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
        if self._state.edit_index is not None:
            self.title = "📝 Редагування нотатки"
            note: Note = self._state.notes_manager.notes[self._state.edit_index]
            self.data = {"text": note.text, "tags": note.tags_string}
            return
        self.title = "📝 Нова нотатка"
        self.data = {"text": "", "tags": ""}

    def _handle_saved(self):
        super().reset()
        SceneFactory.next(SceneType.NOTES_GRID)

    def _ok(self):
        assert self.scene is not None
        self.save()
        if not self.data or not self._validate_form():
            return
        try:
            if self._state.edit_index is None:
                self._state.notes_manager.add_note(self.data)
            else:
                self._state.notes_manager.edit_note(self._state.edit_index, self.data)
            self.scene.add_effect(
                PopUpDialog(
                    self._screen,
                    "✅ Нотатку успішно збережено!",
                    ["Чудово"],
                    on_close=lambda _: self._handle_saved(),
                )
            )
            self._clear_edit_index()
        except Exception as e:
            logger.error("Cannot save Note")
            logger.exception(e)
            self.scene.add_effect(
                PopUpDialog(
                    self._screen, "❌ Помилка збереження Нотатки", ["Спробувати ще раз"]
                )
            )

    def _cancel(self) -> None:
        self._clear_edit_index()
        SceneFactory.next(SceneType.NOTES_GRID)
