from utils.state import AppState
from datetime import datetime
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Layout, Label, Divider, ListBox, Button, TextBox
from asciimatics.exceptions import StopApplication
from cli.tui.scene_type import SceneType
from cli.tui.base_frame import BaseFrame
from factories.scene_factory import SceneFactory

class DashboardView(BaseFrame):
    """Клас-представлення головного дешборду"""

    def __init__(self, screen: Screen, state: AppState) -> None:
        super().__init__(screen, state, title="📊 Personal Assistant")
        self._render_stats()
        self._render_divider()
        self._render_menu()
        self._render_footer()
        self.fix()
        self._birthday_text_box.disabled = True
        self._menu_list_box.focus()
    
    def _render_stats(self) -> None:
        """Верхня секція: Статистика"""
        stats_layout = Layout([1, 1, 1])
        self.add_layout(stats_layout)
        stats = self._state.get_stats()
        stats_layout.add_widget(Label(f"👥 Контактів: {stats['contacts']}"), 0)
        stats_layout.add_widget(Label(f"📝 Нотаток: {stats['notes']}"), 1)
        stats_layout.add_widget(Label(f"📅 Сьогодні: {datetime.now().strftime('%d.%m.%Y')}"), 2)
    
    def _render_menu(self) -> None:
        """Середня секція: Нагадування та Меню"""
        main_layout = Layout([1, 1], fill_frame=True)
        self.add_layout(main_layout)

        # Ліва колонка: Дні народження
        main_layout.add_widget(Label("🎂 НАЙБЛИЖЧІ ДНІ НАРОДЖЕННЯ:"), 0)
        main_layout.add_widget(Divider(draw_line=False), 0)

        self._birthday_text_box = TextBox(
            name="birthday_list",
            height=self.screen.height - 10,
            as_string=True,
            readonly=True
        )
        main_layout.add_widget(self._birthday_text_box, 0)

        # Права колонка: Швидке меню
        main_layout.add_widget(Label("Оберіть дію (використовуйте стрілки та Enter):"), 1)
        main_layout.add_widget(Divider(draw_line=False), 1)

        menu_list_box_options = [
            ("👥 Контакти", SceneType.CONTACTS_GRID),
            ("🎂 Дні народження", SceneType.BIRTHDAYS_GRID),
            ("📝 Нотатки", SceneType.NOTES_GRID),
            ("", ""),
            ("❌ Вихід (Q)", 0)
        ]
        
        self._menu_list_box = ListBox(len(menu_list_box_options),
                                      menu_list_box_options,
                                      name="menu",
                                      on_select=self._on_navigate)
        main_layout.add_widget(self._menu_list_box, 1)
    
    def _render_footer(self) -> None:
        """Нижня секція: Кнопка дії"""
        footer = Layout([1])
        self.add_layout(footer)
        footer.add_widget(Divider())
        footer.add_widget(Button("ПЕРЕЙТИ", self._on_navigate))
    
    def process_event(self, event) -> None:
        if isinstance(event, KeyboardEvent):
            if event.key_code in self._exit_key_codes:
                raise StopApplication("User quit via key code")
        
        return super().process_event(event)
    
    def reset(self) -> None:
        """Метод Frame. Викликається автоматично щоразу при переході на сцену."""
        super().reset()
        self._birthday_text_box.value = '\n'.join(self._state.address_book_manager \
            .get_dashboard_birthdays())

    def _on_navigate(self) -> None:
        """Метод обробки навігації по дешборду"""
        sceneOrExit = self._menu_list_box.value
        if sceneOrExit == 0:
            raise StopApplication("User quit via menu")
        if not sceneOrExit:
            return
        SceneFactory.next(sceneOrExit)
