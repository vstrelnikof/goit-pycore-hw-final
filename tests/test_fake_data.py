from pathlib import Path

import pytest

from models.app_config import AppConfig
from models.app_data_paths import AppDataPaths
from utils.fake_data import create_fakes
from utils.state import AppState


@pytest.fixture
def app_state(tmp_path: Path) -> AppState:
    config = AppConfig(
        app_data_paths=AppDataPaths(
            address_book=tmp_path / "contacts.json",
            notes=tmp_path / "notes.json",
        )
    )
    return AppState(config)


def test_create_fakes_empty_does_nothing(app_state: AppState) -> None:
    create_fakes(app_state, contacts_count=0, notes_count=0)
    assert len(app_state.address_book_manager.contacts) == 0
    assert len(app_state.notes_manager.notes) == 0


def test_create_fakes_contacts_adds_valid_contacts(app_state: AppState) -> None:
    create_fakes(app_state, contacts_count=5, notes_count=0)
    assert len(app_state.address_book_manager.contacts) == 5
    for c in app_state.address_book_manager.contacts:
        assert c.name
        assert c.phone.startswith("+380") and len(c.phone) == 13
        assert c.birthday
    assert len(app_state.notes_manager.notes) == 0


def test_create_fakes_notes_adds_valid_notes(app_state: AppState) -> None:
    create_fakes(app_state, contacts_count=0, notes_count=4)
    assert len(app_state.address_book_manager.contacts) == 0
    assert len(app_state.notes_manager.notes) == 4
    for n in app_state.notes_manager.notes:
        assert n.text.strip()
        assert isinstance(n.tags, list)


def test_create_fakes_both_persisted(app_state: AppState) -> None:
    create_fakes(app_state, contacts_count=2, notes_count=3)
    assert len(app_state.address_book_manager.contacts) == 2
    assert len(app_state.notes_manager.notes) == 3
    app_state.address_book_manager.reload()
    app_state.notes_manager.reload()
    assert len(app_state.address_book_manager.contacts) == 2
    assert len(app_state.notes_manager.notes) == 3
