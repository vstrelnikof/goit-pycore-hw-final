import difflib
from typing import Callable, final
from cli.classic.renderer import Renderer
from utils.state import AppState

# Спеціальне значення, що повертається при команді виходу (exit/quit).
EXIT_SENTINEL = object()

ActionHandler = Callable[[list[str]], str | object]

@final
class CommandDispatcher:
    """Парсинг та виконання команд класичного режиму."""

    def __init__(self, state: AppState) -> None:
        self._state = state
        self._renderer = Renderer()
        self._handlers: dict[str, ActionHandler] = {
            "exit": self._handle_exit,
            "quit": self._handle_exit,
            "help": self._handle_help,
            "contacts": self._handle_contacts,
            "notes": self._handle_notes,
            "birthdays": self._handle_birthdays,
        }

    @staticmethod
    def parse_line(line: str) -> tuple[str, list[str]]:
        """Повертає (команда в нижньому регістрі, список аргументів)."""
        parts = line.strip().split()
        if not parts:
            return ("", [])
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        return (cmd, args)

    def get_suggestion(self, unknown_cmd: str) -> str:
        """Підказка при невідомій команді: найближча команда або порада ввести help."""
        if not unknown_cmd.strip():
            return "💡 Введіть help — список команд."
        known = list(self._handlers.keys())
        matches = difflib.get_close_matches(unknown_cmd.strip().lower(), known, n=1, cutoff=0.4)
        if matches:
            return f"❓ Невідома команда «{unknown_cmd.strip()}». Можливо, ви мали на увазі: {matches[0]}"
        return "❓ Невідома команда. Введіть help — список доступних команд."

    def run(self, cmd: str, args: list[str]) -> str | object:
        """Виконує команду та повертає рядок результату або EXIT_SENTINEL."""
        handler = self._handlers.get(cmd)
        if handler is None:
            return self.get_suggestion(cmd)
        return handler(args)

    def _handle_exit(self, args: list[str]) -> object:
        return EXIT_SENTINEL

    def _handle_help(self, args: list[str]) -> str:
        return self._run_help()

    def _handle_contacts(self, args: list[str]) -> str:
        search_term = args[0] if args else ""
        rows = self._state.address_book_manager.get_contacts_table_data(search_term)
        return self._renderer.format_contacts_table(rows)

    def _handle_notes(self, args: list[str]) -> str:
        search_term = args[0] if args else ""
        rows = self._state.notes_manager.get_notes_table_data(search_term)
        return self._renderer.format_notes_table(rows)

    def _handle_birthdays(self, args: list[str]) -> str:
        try:
            days = int(args[0]) if args else 7
        except ValueError:
            days = 7
        rows = self._state.address_book_manager.get_birthdays_table_data(days)
        return self._renderer.format_birthdays_table(rows)

    def _run_help(self) -> str:
        help_lines = [
            "📖 Доступні команди:",
            "  👥 contacts [пошук] — список контактів",
            "  📝 notes [пошук]    — список нотаток",
            "  🎂 birthdays [днів] — іменинники на N днів",
            "  ❓ help             — ця підказка",
            "  👋 exit / quit      — вихід",
        ]
        return "\n".join(help_lines)
