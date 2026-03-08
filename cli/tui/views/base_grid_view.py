from factories.scene_factory import SceneFactory
from utils.state import AppState
from abc import abstractmethod
from cli.tui.base_frame import BaseFrame
from asciimatics.screen import Screen
from asciimatics.widgets import (
    Layout,
    MultiColumnListBox,
    Button,
    Divider,
    Text,
    PopUpDialog,
)
from enums.scene_type import SceneType


class BaseGridView(BaseFrame):
    """Архі-клас для реалізації вікон із таблицею, елементами управління та пошуком"""

    _list_box: MultiColumnListBox
    _is_search_enabled: bool = True
    _is_create_enabled: bool = False
    _is_update_enabled: bool = False
    _is_delete_enabled: bool = False

    def __init__(self, screen: Screen, state: AppState, **kwargs) -> None:
        super().__init__(screen, state, has_border=True, **kwargs)
        if self._is_search_enabled:
            search_layout = Layout([1, 10, 1])
            self.add_layout(search_layout)
            self._search_box = Text(
                "🔎 Пошук: ", name="search", on_change=self._filter_list
            )
            search_layout.add_widget(self._search_box, 1)
        self._render_content()
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Divider())
        button_layout = Layout([1, 1, 1, 1])
        self.add_layout(button_layout)
        if self._is_create_enabled:
            button_layout.add_widget(Button("Створити", self._on_create), 0)
        if self._is_update_enabled:
            button_layout.add_widget(Button("Редагувати", self._on_edit), 1)
        if self._is_delete_enabled:
            button_layout.add_widget(Button("Видалити", self._on_delete), 2)
        button_layout.add_widget(Button("Назад (ESC)", self._on_back), 3)
        self.fix()

    @abstractmethod
    def _render_content(self) -> None:
        """Абстрактний метод, реалізація якого має будувати розмітку основного блоку вікна"""
        pass

    @abstractmethod
    def _filter_list(self) -> None:
        """Абстрактний метод для реалізації фільтрації на основі тексту в пошуку"""
        pass

    def _on_create(self) -> None:
        pass

    def _on_edit(self) -> None:
        if self._list_box.value is None:
            return
        self._state.edit_index = self._list_box.value

    def _on_delete(self) -> None:
        assert self.scene is not None
        if self._list_box.value is None:
            return
        self.scene.add_effect(
            PopUpDialog(
                self._screen,
                "❓ Ви впевнені, що хочете видалити запис?",
                ["Так", "Ні"],
                on_close=self._confirm_delete,
            )
        )

    def _confirm_delete(self, selected_button_idx: int) -> None:
        pass

    def _on_back(self) -> None:
        SceneFactory.next(SceneType.MAIN)

    def reset(self):
        """Метод Frame. Викликається автоматично щоразу при переході на сцену."""
        super().reset()
        self._filter_list()
