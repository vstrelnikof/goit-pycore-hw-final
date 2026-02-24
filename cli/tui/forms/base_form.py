from utils.state import AppState
from abc import abstractmethod
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, Button, PopUpDialog, Divider, Widget
from cli.tui.base_frame import BaseFrame
from cli.tui.scene_type import SceneType
from factories.scene_factory import SceneFactory

class BaseForm(BaseFrame):
    """Архі-клас для реалізації модальних вікон із формою та елементами управління"""

    _required_fields: list[str] = []

    def __init__(self, screen: Screen, state: AppState, **kwargs) -> None:
        super().__init__(screen, state,
                         height=screen.height // 2,
                         width=screen.width // 2,
                         has_shadow=True,
                         is_modal=True,
                         **kwargs)
        self._render_content()
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout = Layout([1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Зберегти", self._ok), 0)
        layout.add_widget(Button("Скасувати (ESC)", self._cancel), 1)
        self.fix()

    @abstractmethod
    def _render_content(self) -> None:
        """Абстрактний метод, реалізація якого має будувати розмітку основного блоку вікна"""
        pass

    def reset(self) -> None:
        """Метод Frame. Викликається автоматично щоразу при переході на сцену."""
        super().reset()

    def _validate_form(self) -> bool:
        assert self.scene is not None
        assert self.data is not None

        errors: list[str] = []
        for field_name, _ in self.data.items():
            widget: Widget | None = self.find_widget(field_name)

            if not widget:
                continue

            if field_name in self._required_fields and not widget.value:
                errors.append(f"Поле '{widget.label}' є обов'язковим!")
            elif hasattr(widget, "is_valid") and not widget.is_valid:
                errors.append(f"Поле '{widget.label}' заповнено некоректно!")

        has_errors = bool(errors)

        if has_errors:
            self.scene.add_effect(
                PopUpDialog(self._screen, '\n'.join(errors), ["Виправити"])
            )

        return not has_errors
    
    def _clear_edit_index(self):
        self._state.edit_index = None

    def _ok(self) -> None:
        self.save()
        self._clear_edit_index()

    def _cancel(self) -> None:
        self._clear_edit_index()
        SceneFactory.next(SceneType.MAIN)
