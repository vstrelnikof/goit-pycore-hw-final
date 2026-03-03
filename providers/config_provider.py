import logging
import yaml
from pathlib import Path
from models.app_config import AppConfig

class ConfigProvider:
    """Провайдер конфігурації застосунку через файл"""

    @staticmethod
    def load() -> AppConfig:
        """Фабричний метод який читає конфігурацію із файлу"""
        config_path = Path("config.yaml")
        default_app_cfg = AppConfig()
        if not config_path.exists():
            logging.warning("Config file not found: %s", config_path)
            return default_app_cfg
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                return AppConfig(**config.get("app", {}))
        except Exception as e:
            logging.error("Cannot create application config")
            logging.exception(e)
            return default_app_cfg
