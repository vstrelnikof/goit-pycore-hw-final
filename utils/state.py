from typing import final
from models.app_config import AppConfig
from providers.storage_provider import StorageProvider
from services.address_book_service import AddressBookService
from services.notes_service import NotesService


@final
class AppState:
    """Об'єкт стану, що зберігає екземпляри сервісів,
    провайдерів та глобальні налаштування."""

    def __init__(self, app_config: AppConfig) -> None:
        self.tui_theme = app_config.theme
        address_book_storage_provider = StorageProvider(
            app_config.app_data_paths.address_book
        )
        self.address_book_manager = AddressBookService(address_book_storage_provider)
        notes_storage_provider = StorageProvider(app_config.app_data_paths.notes)
        self.notes_manager = NotesService(notes_storage_provider)
        self.edit_index: int | None = (
            None  # Сховище для позиції елемента який редагується
        )

    def get_stats(self) -> dict[str, int]:
        """Поточна кількість контактів та нотаток"""
        return {
            "contacts": len(self.address_book_manager.contacts),
            "notes": len(self.notes_manager.notes),
        }
