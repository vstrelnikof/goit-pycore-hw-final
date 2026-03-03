from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, MultiColumnListBox
from cli.tui.views.base_grid_view import BaseGridView
from enums.scene_type import SceneType
from factories.scene_factory import SceneFactory

class ContactGridView(BaseGridView):
    """Клас-представлення таблиці контактів"""

    _is_create_enabled: bool = True
    _is_update_enabled: bool = True
    _is_delete_enabled: bool = True

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, 
                         title="🔍 Пошук та Управління Контактами")
    
    def _render_content(self) -> None:
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        self._list_box = MultiColumnListBox(
            name="contact_list",
            height=self.screen.height - 5,
            columns=["<25%", "<20%", "<20%", "<20%", "<15%"],
            titles=["👤 Ім'я", "📱 Телефон", "📧 Email", "🏠 Адреса", "🎂 Дата"],
            options=[],
            on_select=self._on_edit
        )
        list_layout.add_widget(self._list_box)

    def _filter_list(self):
        search_term = self._search_box.value.lower() \
            if self._search_box.value else ""
        self._list_box.options = self._state.address_book_manager \
            .get_contacts_table_data(search_term)
    
    def _on_create(self) -> None:
        super()._on_create()
        SceneFactory.next(SceneType.CONTACT_FORM)
    
    def _on_edit(self) -> None:
        super()._on_edit()
        SceneFactory.next(SceneType.CONTACT_FORM)

    def _confirm_delete(self, selected_button_idx: int) -> None:
        if self._is_popup_confirmed(selected_button_idx):
            index = self._list_box.value
            if (index is None):
                raise ValueError("selected_button_idx is None")
            self._state.address_book_manager.delete_contact(index)
            self._filter_list() # Оновлюємо таблицю
