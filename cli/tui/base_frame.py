from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Frame
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from cli.tui.scene_type import SceneType

class BaseFrame(Frame):
    """Архі-клас для реалізації вікон"""
    _exit_key_codes: list[int] = [ord('q'), ord('Q'), ord('й'), ord('Й')]
    _esc_key_path: str = SceneType.MAIN

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

    def process_event(self, event) -> None:
        """Глобальний обробник подій із периферійних пристроїв"""
        if isinstance(event, KeyboardEvent):
            if event.key_code == -1:
                self._state.edit_index = None
                raise NextScene(self._esc_key_path)
        
        return super().process_event(event)
