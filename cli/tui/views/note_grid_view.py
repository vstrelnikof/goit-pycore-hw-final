from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, MultiColumnListBox, Text, CheckBox
from enums.scene_type import SceneType
from cli.tui.views.base_grid_view import BaseGridView
from factories.scene_factory import SceneFactory


class NoteGridView(BaseGridView):
    """Клас-представлення таблиці нотаток"""

    _is_search_enabled: bool = False
    _is_create_enabled: bool = True
    _is_update_enabled: bool = True
    _is_delete_enabled: bool = True

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, title="📓 Ваші нотатки")

    def _render_content(self) -> None:
        search_layout = Layout([1, 6, 2, 1])
        self.add_layout(search_layout)
        self._search_box = Text(
            "🔎 Пошук: ", name="search", on_change=self._filter_list
        )
        search_layout.add_widget(self._search_box, 1)
        self._sort_check_box = CheckBox(" ↕", name="sort", on_change=self._filter_list)
        search_layout.add_widget(self._sort_check_box, 2)
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        self._list_box = MultiColumnListBox(
            name="notes_list",
            height=self.screen.height - 5,
            columns=["^70%", "<30%"],
            titles=["📝 Зміст нотатки", "🔖 Теги"],
            options=[],
            on_select=self._on_edit,
        )
        list_layout.add_widget(self._list_box)

    def _filter_list(self):
        search_term = self._search_box.value.lower() if self._search_box.value else ""
        is_sort_checked: bool = self._sort_check_box.value
        table_data = self._state.notes_manager.get_notes_table_data(
            search_term, is_sort_checked
        )
        self._list_box.options = [row.to_tuple() for row in table_data]
        # scroll_to_index does not exist in MultiColumnListBox.
        # To emulate going to the top, set value to first index if any options exist.
        if self._list_box.options:
            self._list_box.value = self._list_box.options[0][1]
        else:
            self._list_box.value = None

    def _on_create(self) -> None:
        super()._on_create()
        SceneFactory.next(SceneType.NOTE_FORM)

    def _on_edit(self) -> None:
        super()._on_edit()
        SceneFactory.next(SceneType.NOTE_FORM)

    def _confirm_delete(self, selected_button_idx: int) -> None:
        if self._is_popup_confirmed(selected_button_idx):
            id = self._list_box.value
            if id is None:
                raise ValueError("selected_button_idx is None")
            self._state.notes_manager.delete_note(id)
            self._filter_list()  # Оновлюємо таблицю
