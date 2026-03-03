from pathlib import Path
import pytest
from models.app_config import AppConfig
from models.app_data_paths import AppDataPaths
from services.address_book_service import AddressBookService
from services.notes_service import NotesService
from utils.state import AppState

@pytest.fixture
def app_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AppState:
    # Працюємо в тимчасовій директорії, щоб не торкатись реальних файлів
    monkeypatch.chdir(tmp_path)
    paths = AppDataPaths(
        address_book=tmp_path / "contacts.json",
        notes=tmp_path / "notes.json",
    )
    config = AppConfig(app_data_paths=paths)
    return AppState(config)

def test_app_state_initializes_services_and_theme(app_state: AppState) -> None:
    assert isinstance(app_state.address_book_manager, AddressBookService)
    assert isinstance(app_state.notes_manager, NotesService)
    # Тема береться із конфіґу
    assert app_state.tui_theme == AppConfig().theme
    # За замовчуванням жоден елемент не редагується
    assert app_state.edit_index is None

def test_get_stats_reflects_current_counts(app_state: AppState) -> None:
    # Початково обидва списки порожні
    assert app_state.get_stats() == {"contacts": 0, "notes": 0}

    # Підставляємо довільні об'єкти, нам важлива лише кількість
    app_state.address_book_manager.contacts = [object(), object()]
    app_state.notes_manager.notes = [object()]

    stats = app_state.get_stats()
    assert stats["contacts"] == 2
    assert stats["notes"] == 1

