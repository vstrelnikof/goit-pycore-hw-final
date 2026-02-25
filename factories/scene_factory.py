from typing import final
from asciimatics.exceptions import NextScene
from asciimatics.scene import Scene
from cli.tui.base_frame import BaseFrame
from cli.tui.scene_type import SceneType

@final
class SceneFactory:
    """Фабрика для створення сцен asciimatics"""

    @staticmethod
    def next(scene_type: SceneType):
        """Статичний метод який створює сцену по типу"""
        raise NextScene(scene_type)

    @staticmethod
    def createScenes(frames: dict[SceneType, BaseFrame]) -> list[Scene]:
        """Статичний метод який створює список сцен за типами"""
        return [
            Scene(effects=[frame],
                  duration=-1,
                  name=scene_type)
            for scene_type, frame in frames.items()
        ]