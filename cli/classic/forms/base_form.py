from abc import ABC, abstractmethod

from cli.classic.colors import Colors


class FormCancelledError(Exception):
    """Виникає, коли користувач відміняє введення форми (q / cancel)."""

    pass


class ConsoleFormBase(ABC):
    """Базова консольна форма з підтримкою відміни (q / cancel)."""

    # Ключові слова для виходу з форми без збереження
    CANCEL_KEYS = ("q", "cancel")

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def _is_cancel(self, value: str) -> bool:
        """Чи означає введений рядок бажання скасувати форму."""
        return value.strip().lower() in self.CANCEL_KEYS

    def _print_cancel_hint(self) -> None:
        """Виводить підказку про можливість відміни."""
        print(Colors.dim("  (введіть q або cancel для відміни)"))

    def _read_field(self, prompt: str, default: str = "") -> str:
        """
        Зчитує один рядок з консолі. При відміні (q/cancel) викидає FormCancelledError.
        Інакше повертає введений текст або default при порожньому вводі.
        """
        value = input(Colors.accent(prompt)).strip() or default
        if self._is_cancel(value):
            raise FormCancelledError
        return value

    def _read_line_or_raise(self, prompt: str = "│ ") -> str:
        """
        Зчитує один рядок без обрізання пробілів (для багаторядкового вводу).
        При відміні (q/cancel) викидає FormCancelledError.
        """
        line = input(Colors.dim(prompt))
        if self._is_cancel(line):
            raise FormCancelledError
        return line

    @abstractmethod
    def prompt(self) -> dict:
        """Збирає дані форми через консоль. При відміні користувачем викидає FormCancelledError."""
        pass
