import logging
import yaml
from pathlib import Path
from models.app_config import AppConfig

class ConfigProvider:
    """Провайдер конфігурації застосунку через файл"""

    @staticmethod
    def load() -> AppConfig:
        """Фабричний метод який читає конфігурацію із файлу та ініціалізує @AppConfig"""
        config_path = Path("config.yaml")
        default_app_cfg = AppConfig.default()
        if not config_path.exists():
            logging.warning("Config file not found: %s", config_path)
            return default_app_cfg
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        except Exception as e:
            logging.error("Cannot read config file")
            logging.exception(e)
            return default_app_cfg
        app_cfg = config.get("app", {})
        tui_cfg = app_cfg.get("tui", {})
        theme = str(tui_cfg.get("theme", default_app_cfg.theme))
        log_level = int(app_cfg.get("log_level", default_app_cfg.log_level))
        return AppConfig(theme=theme, log_level=log_level)