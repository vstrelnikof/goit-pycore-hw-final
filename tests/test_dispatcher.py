from pathlib import Path
import pytest
from cli.classic.dispatcher import CommandDispatcher
from cli.classic.handler import CommandHandler
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider
from utils.state import AppState


@pytest.fixture
def app_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AppState:
    monkeypatch.chdir(tmp_path)
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
    msg = d.get_unknown_message("contacs")
    assert "contacs" in msg
    assert "contacts" in msg


def test_get_suggestion_returns_help_hint_when_no_match() -> None:
    state = AppState(AppConfig())
    d = CommandDispatcher(state)
    msg = d.get_unknown_message("xyz")
    assert "help" in msg.lower()


def test_run_unknown_command_returns_suggestion() -> None:
    state = AppState(AppConfig())
    d = CommandDispatcher(state)
    result = d.run("unknown", [])
    assert "unknown" in result or "Невідома" in result


def test_run_exit_returns_sentinel(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    assert d.run("exit", []) == CommandDispatcher.EXIT_SENTINEL
    assert d.run("quit", []) == CommandDispatcher.EXIT_SENTINEL


def test_run_help_returns_help_text(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("help", [])
    assert "contacts" in result
    assert "notes" in result
    assert "exit" in result


def test_run_contacts_without_subcommand_returns_suggestion(
    app_state: AppState,
) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("contacts", [])
    assert isinstance(result, str) and len(result) > 0
    assert "Підкоманди" in result or "search" in result


def test_run_notes_show_returns_full_note_or_error(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    # Очищаємо нотатки, щоб індекс 0 спочатку не існував
    app_state.notes_manager.notes.clear()
    result = d.run("notes", ["show", "0"])
    assert "Нотатку з таким індексом не знайдено" in result
    # Додаємо нотатку і переглядаємо
    app_state.notes_manager.add_note(
        {"text": "Тестова нотатка для перегляду.", "tags": "тест"}
    )
    result = d.run("notes", ["show", "0"])
    assert "Тестова нотатка для перегляду" in result
    assert "тест" in result


def test_parse_search_and_limit_empty_returns_empty_and_none() -> None:
    assert CommandHandler.parse_search_and_limit([]) == ("", None)


def test_parse_search_and_limit_single_number_is_limit() -> None:
    assert CommandHandler.parse_search_and_limit(["5"]) == ("", 5)


def test_parse_search_and_limit_single_word_is_search() -> None:
    assert CommandHandler.parse_search_and_limit(["john"]) == ("john", None)


def test_parse_search_and_limit_search_and_number() -> None:
    assert CommandHandler.parse_search_and_limit(["john", "10"]) == ("john", 10)


def test_parse_search_and_limit_multiple_words_and_number() -> None:
    assert CommandHandler.parse_search_and_limit(["a", "b", "3"]) == ("a b", 3)


def test_run_contacts_with_limit_shows_footer(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    for i in range(3):
        app_state.address_book_manager.add_contact(
            {
                "name": f"User{i}",
                "phone": "",
                "email": "",
                "address": "",
                "birthday": "",
            }
        )
    result = d.run("contacts", ["search", "2"])
    assert "Показано 2 з 3" in result


def test_run_notes_with_limit_shows_footer(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    for i in range(3):
        app_state.notes_manager.add_note({"text": f"Note {i}", "tags": ""})
    result = d.run("notes", ["search", "2"])
    assert "Показано 2 з 3" in result


def test_run_contacts_unknown_subcommand_returns_suggestion(
    app_state: AppState,
) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("contacts", ["xyz"])
    assert "Підкоманди" in result or "Введіть одну з" in result


def test_run_notes_fuzzy_show_executes(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    app_state.notes_manager.add_note({"text": "Тестова нотатка", "tags": "тег"})
    result = d.run("notes", ["shw", "0"])
    assert "Тестова нотатка" in result


def test_run_contacts_fuzzy_edit_executes(app_state: AppState) -> None:
    d = CommandDispatcher(app_state)
    result = d.run("contacts", ["edi", "0"])
    assert "Контакт з таким індексом не знайдено" in result
