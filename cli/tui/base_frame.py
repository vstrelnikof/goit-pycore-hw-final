from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Divider
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from cli.tui.scene_type import SceneType

class BaseFrame(Frame):
    """Архі-клас для реалізації вікон (фреймів)"""

    def __init__(self, screen: Screen, state: AppState, **kwargs) -> None:
        # Словник використовується для перекриття значень на кожному
        # рівні наслідування
        super().__init__(**{
            "screen": screen,
            "height": screen.height,
            "width": screen.width, 
            "has_border": True,
            "reduce_cpu": True,
            **kwargs,
        })
        self._state = state
        self.set_theme(state.tui_theme)

    @property
    def _exit_key_codes(self) -> list[int]:
        """Віртуальна властивість, реалізація якої вказує на
        Unicode символи клавіш для виходу"""
        return [ord('q'), ord('Q'), ord('й'), ord('Й')]
    
    @property
    def _esc_key_path(self) -> SceneType:
        """Віртуальна властивість, реалізація якої вказує на тип сцени по ESC"""
        return SceneType.MAIN

    def process_event(self, event) -> None:
        """Глобальний обробник подій із периферійних пристроїв"""
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1:
                self._state.edit_index = None
                raise NextScene(self._esc_key_path)
        
        return super().process_event(event)

    def _render_divider(self) -> None:
        """Рендерить горизонтальний розділювач"""
        divider_layout = Layout([1])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())

    def _is_popup_confirmed(self, selected_button_idx: int) -> bool:
        """В модальному діалозі відповідає кнопці \"Так\""""
        return selected_button_idx == 0