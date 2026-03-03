import json
import logging
from pathlib import Path
from typing import Any, Generator
from decorators.log_action import log_action

class StorageProvider:
    """Провайдер сховища (поки тільки JSON)"""

    def __init__(self, filename: str, encoding: str = "utf-8") -> None:
        self.file_encoding = encoding
        self.file = Path("data") / filename
        self.file.parent.mkdir(exist_ok=True)
        if not self.file.exists():
            self.save([])

    def load(self) -> Generator:
        """Генератор для построчного читання JSON файлу"""
        with self.file.open("r", encoding=self.file_encoding) as f:
            data = json.load(f)
            for item in data:
                yield item

    @log_action(level=logging.DEBUG, log_time=True)
    def save(self, data: Any) -> None:
        """Збереження будь якої структури в JSON файл"""
        with self.file.open("w", encoding=self.file_encoding) as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
