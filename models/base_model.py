import logging
from dataclasses import asdict, dataclass, field
from abc import ABC, abstractmethod
from typing import final
from uuid import UUID, uuid4

@dataclass(kw_only=True)
class BaseModel(ABC):
    """Архі-тип для реалізації моделі даних"""
    id: UUID = field(default_factory=uuid4)

    @final
    def is_valid(self) -> bool:
        """Метод який фактично валідує модель та обробляє результат"""
        validation_result: dict = self._validate()
        is_failed: bool = any(result for _, result in validation_result.items()
                              if not result)
        if is_failed:
            logging.warning(f"Model validation failed: {str(validation_result)}")
        return not is_failed
    
    def to_dict(self) -> dict:
        """Перетворює модель у словник, придатний для JSON"""
        data: dict = asdict(self)
        data['id'] = str(self.id)
        return data

    @abstractmethod
    def _validate(self) -> dict[str, bool]:
        """Абстрактний метод для реалізації перевірки відповідної даних моделі"""
        pass
    
    @classmethod
    def from_dict(cls, data: dict):
        """Віртуальний фабричний метод для створення екземпляру із словника (форми)"""
        return cls(**data)
