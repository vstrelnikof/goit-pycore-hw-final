import difflib
from typing import Callable, final

from cli.classic.handler import CommandHandler
from utils.state import AppState


ActionHandler = Callable[[list[str]], str | object]


@final
class CommandDispatcher:
    """Парсинг та маршрутизація команд класичного режиму. Виконання делеговане CommandHandler."""

    # Спеціальне значення, що повертається при команді виходу (exit/quit).
    EXIT_SENTINEL = object()
    # Коефіцієнт схожості для fuzzy-збігу команд.
    SUBCMD_CUTOFF = 0.4

    def __init__(self, state: AppState) -> None:
        self._state = state
        self._handler = CommandHandler(state)
        self._handlers: dict[str, ActionHandler] = {
            "dashboard": self._handler.handle_dashboard,
            "stats": self._handler.handle_dashboard,
            "exit": self._handle_exit,
            "quit": self._handle_exit,
            "help": self._handler.handle_help,
            "contacts": self._handler.handle_contacts,
            "notes": self._handler.handle_notes,
            "birthdays": self._handler.handle_birthdays,
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
        """Підказка при невідомій команді першого рівня: найближча команда або порада ввести help."""
        if not unknown_cmd.strip():
            return "💡 Введіть help — список команд."
        known = list(self._handlers.keys())
        matches = difflib.get_close_matches(
            unknown_cmd.strip().lower(), known, n=1, cutoff=self.SUBCMD_CUTOFF
        )
        if matches:
            return f"❓ Невідома команда «{unknown_cmd.strip()}». Можливо, ви мали на увазі: {matches[0]}"
        return "❓ Невідома команда. Введіть help — список доступних команд."

    def run(self, cmd: str, args: list[str]) -> str | object:
        """Виконує команду та повертає рядок результату або EXIT_SENTINEL."""
        handler = self._handlers.get(cmd)
        if handler is not None:
            return handler(args)

        # Невідома команда: якщо є одна близька — виконуємо її
        if cmd.strip():
            known = list(self._handlers.keys())
            matches = difflib.get_close_matches(
                cmd.strip().lower(), known, n=1, cutoff=self.SUBCMD_CUTOFF
            )
            if len(matches) == 1:
                return self._handlers[matches[0]](args)

        return self.get_suggestion(cmd)

    def _handle_exit(self, args: list[str]) -> object:
        return self.EXIT_SENTINEL
