from dataclasses import dataclass
import logging
from typing import final

@final
@dataclass
class AppConfig:
    """Модель конфігу застосунку"""
    theme: str
    log_level: int

    @classmethod
    def default(cls):
        """Фабричний метод для створення екземпляру за замовчуванням"""
        return AppConfig(theme="default", log_level=logging.INFO)