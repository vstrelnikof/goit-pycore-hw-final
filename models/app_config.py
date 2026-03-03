import logging
from typing import final
from pydantic import BaseModel
from enums.theme_type import ThemeType

@final
class AppConfig(BaseModel):
    """Модель конфігу застосунку"""
    log_level: int = logging.INFO
    theme: ThemeType = ThemeType.DEFAULT
