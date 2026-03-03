import logging
import yaml
from argparse import ArgumentParser, Namespace as ArgsNamespace
from pathlib import Path
from models.app_config import AppConfig

logger = logging.getLogger(__name__)

class ConfigProvider:
    """Провайдер конфігурації застосунку через файл та через аргументи командного рядка"""

    @staticmethod
    def load() -> AppConfig:
        """Фабричний метод який читає конфігурацію"""
        config_path = Path("config.yaml")
        default_config = AppConfig()
        if not config_path.exists():
            logger.warning("Config file not found: %s", config_path)
            return default_config
        try:
            args_config = ConfigProvider.__get_app_args()
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = yaml.safe_load(f) or {}
                merged_config = ConfigProvider.__get_merged_settings(
                    file_config, args_config, default_config)
                return AppConfig(**merged_config)
        except Exception as e:
            logger.error("Cannot create application config")
            logger.exception(e)
            return default_config

    @staticmethod
    def __get_app_args() -> ArgsNamespace:
        """Метод парсить налаштування із аргументів командного рядка"""
        parser = ArgumentParser(description="Personal assistant configuration")
        parser.add_argument("--theme", type=str, help="Personal assistant theme")
        parser.add_argument("--log-level", type=int, help="Logging level")
        args = parser.parse_args()
        return args
    
    @staticmethod
    def __get_merged_settings(file_config: dict, args_config: ArgsNamespace, default: AppConfig) -> dict:
        """Метод мержить налаштування із конфіг-файлу та із аргументів командного рядка"""
        merged = dict(file_config.get("app", default.__dict__))
        for k, v in vars(args_config).items():
            if v is not None:
                merged[k] = v
        return merged
