import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import final
from uuid import uuid4

@dataclass
class BaseModel(ABC):
    """Архі-тип для реалізації моделі даних"""

    def __init__(self) -> None:
        self.id = uuid4()

    @final
    def is_valid(self) -> bool:
        """Метод який фактично валідує модель та обробляє результат"""
        validation_result: dict = self._validate()
        is_failed: bool = any(result for _, result in validation_result.items()
                              if not result)
        if is_failed:
            logging.warning(f"Model validation failed: {str(validation_result)}")
        return not is_failed

    @abstractmethod
    def _validate(self) -> dict[str, bool]:
        """Абстрактний метод для реалізації перевірки відповідної даних моделі"""
        pass
