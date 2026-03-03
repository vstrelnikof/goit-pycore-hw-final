import logging
from typing import final
from pydantic import BaseModel
from enums.theme_type import ThemeType
from models.app_data_paths import AppDataPaths

@final
class AppConfig(BaseModel):
    """Модель конфігу застосунку"""
    log_level: int = logging.INFO
    theme: ThemeType = ThemeType.DEFAULT
    app_data_paths: AppDataPaths = AppDataPaths()
