from asciimatics.screen import Screen
from asciimatics.widgets import Layout, MultiColumnListBox, Text
from cli.tui.views.base_grid_view import BaseGridView
from utils.state import AppState
from utils.validator import Validator
from helpers.date_helpers import days_left_in_year

class BirthdayGridView(BaseGridView):
    """Клас-представлення таблиці днів народження"""

    _is_search_enabled = False

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, 
                         title="🎂 Дні народження")
    
    def _render_content(self) -> None:
        days_layout = Layout([1, 10, 1])
        self.add_layout(days_layout)
        self._search_box = Text("🔎 Кількість днів: ", name="search",
                                on_change=self._filter_list,
                                validator=lambda days_string:
                               not days_string or Validator.validate_days(days_string))
        days_layout.add_widget(self._search_box, 1)

        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)

        self._list_box = MultiColumnListBox(
            name="birthday_list",
            height=self.screen.height - 5,
            columns=["<15%", "<25%", "<20%", "<20%", "<20%"],
            titles=["🎂 Дата", "👤 Ім'я", "📱 Телефон", "📧 Email", "🏠 Адреса"],
            options=[], # Спочатку порожній, заповниться в _filter_list
        )
        list_layout.add_widget(self._list_box)

    def _filter_list(self):
        days_to_show: int | None = int(self._search_box.value) \
            if self._search_box.value.isnumeric() else days_left_in_year()
        table_data = self._state.address_book_manager \
            .get_birthdays_table_data(days_to_show)
        self._list_box.options = [row.to_tuple() for row in table_data]
