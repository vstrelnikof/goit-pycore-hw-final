from pathlib import Path
import pytest
from cli.classic.dispatcher import EXIT_SENTINEL, CommandDispatcher
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider
from utils.state import AppState

@pytest.fixture
def app_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AppState:
    monkeypatch.setattr("sys.argv", ["pytest"])
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n"
        "  log_level: 20\n"
        "  app_data_paths:\n"
        "    address_book: data/contacts.json\n"
        "    notes: data/notes.json\n",
        encoding="utf-8",
    )
    config = ConfigProvider.load(config_path)
    return AppState(config)

def test_parse_line_returns_lowercase_command_and_args() -> None:
    cmd, args = CommandDispatcher.parse_line("  Contacts  john  ")
    assert cmd == "contacts"
    assert args == ["john"]

def test_parse_line_empty_returns_empty_command_and_args() -> None:
    cmd, args = CommandDispatcher.parse_line("   ")
    assert cmd == ""
    assert args == []

def test_get_suggestion_returns_matches_when_similar() -> None:
    state = AppState(AppConfig())
    d = CommandDispatcher(state)
    msg = d.get_suggestion("contacs")
    assert "contacs" in msg
    assert "contacts" in msg

def test_get_suggestion_returns_help_hint_when_no_match() -> None:
    state = AppState(AppConfig())
    d = CommandDispatcher(state)
    msg = d.get_suggestion("xyz")
    assert "help" in msg.lower()

def test_run_unknown_command_returns_suggestion() -> None:
    state = AppState(AppConfig())
    d = CommandDispatcher(state)
    result = d.run("unknown", [])
    assert "unknown" in result or "Невідома" in result

def test_run_exit_returns_sentinel(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    assert d.run("exit", []) == EXIT_SENTINEL
    assert d.run("quit", []) == EXIT_SENTINEL

def test_run_help_returns_help_text(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("help", [])
    assert "contacts" in result
    assert "notes" in result
    assert "exit" in result

def test_run_contacts_returns_table_or_empty(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("contacts", [])
    assert isinstance(result, str) and len(result) > 0
    # Повертається або таблиця (є цифра індексу або переноси рядків), або текст повідомлення
    assert "\n" in result or "0" in result or "1" in result

def test_run_notes_show_returns_full_note_or_error(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    # Очищаємо нотатки, щоб індекс 0 спочатку не існував
    app_state.notes_manager.notes.clear()
    result = d.run("notes", ["show", "0"])
    assert "Нотатку з таким індексом не знайдено" in result
    # Додаємо нотатку і переглядаємо
    app_state.notes_manager.add_note({"text": "Тестова нотатка для перегляду.", "tags": "тест"})
    result = d.run("notes", ["show", "0"])
    assert "Тестова нотатка для перегляду" in result
    assert "тест" in result
