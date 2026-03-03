import json
import logging
from pathlib import Path
from typing import Any, Generator, List, Union
from decorators.log_action import log_action

logger = logging.getLogger(__name__)

class StorageProvider:
    """Провайдер сховища (поки тільки JSON)"""

    def __init__(self, file: Path, encoding: str = "utf-8") -> None:
        self.file_encoding = encoding
        self.file = file
        self.file.parent.mkdir(parents=True, exist_ok=True)
        if not self.file.exists():
            self.save([])

    def load_list(self) -> Generator[Any, None, None]:
        """Генератор для построчного читання масиву з JSON файлу"""
        try:
            with self.file.open("r", encoding=self.file_encoding) as f:
                data: Union[List[Any], Any] = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        yield item
                else:
                    logger.warning("JSON is not an array")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"Error reading file: {e}")

    @log_action(level=logging.DEBUG, log_time=True)
    def save(self, data: Any) -> None:
        """Збереження будь-якої структури в JSON файл"""
        try:
            with self.file.open("w", encoding=self.file_encoding) as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.debug(f"File \"{self.file}\" saved successfully")
        except Exception as e:
            logger.error(f"Error saving file: {e}")