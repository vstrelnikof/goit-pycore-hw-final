from abc import abstractmethod
from providers.storage_provider import StorageProvider


class BaseService:
    """Архі-клас для реалізації сервісу"""

    # Порядок літер українського алфавіту для коректного сортування (не за Unicode).
    _ukrainian_alphabet = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"

    def __init__(self, storage_provider: StorageProvider) -> None:
        self.storage = storage_provider
        self.reload()

    @abstractmethod
    def save(self):
        """Абстрактний метод для реалізації збереження даних у відповідне сховище"""
        pass

    @abstractmethod
    def reload(self):
        """Абстрактний метод для реалізації завантаження даних із відповідного сховища"""
        pass

    @staticmethod
    def _ukrainian_sort_key(name: str) -> tuple:
        """Повертає ключ для сортування за українським алфавітом (А, Б, В, Г, Ґ, Д, …)."""
        return tuple(
            BaseService._ukrainian_alphabet.index(c.upper())
            if c.upper() in BaseService._ukrainian_alphabet
            else (1000 + ord(c))
            for c in name
        )
