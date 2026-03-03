from abc import abstractmethod
from providers.storage_provider import StorageProvider

class BaseService:
    """Архі-клас для реалізації сервісу"""

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