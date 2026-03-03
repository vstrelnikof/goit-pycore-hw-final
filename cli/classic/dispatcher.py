import difflib
from typing import Callable, final
from cli.classic.renderer import Renderer
from cli.classic.forms import ContactConsoleForm, NoteConsoleForm
from utils.state import AppState

# Спеціальне значення, що повертається при команді виходу (exit/quit).
EXIT_SENTINEL = object()

ActionHandler = Callable[[list[str]], str | object]

@final
class CommandDispatcher:
    """Парсинг та виконання команд класичного режиму"""

    def __init__(self, state: AppState) -> None:
        self._state = state
        self._renderer = Renderer()
        self._handlers: dict[str, ActionHandler] = {
            "dashboard": self._handle_dashboard,
            "stats": self._handle_dashboard,
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
        if handler is not None:
            return handler(args)

        # Невідома команда: якщо є одна близька — виконуємо її
        if cmd.strip():
            known = list(self._handlers.keys())
            matches = difflib.get_close_matches(cmd.strip().lower(), known, n=1, cutoff=0.4)
            if len(matches) == 1:
                return self._handlers[matches[0]](args)

        return self.get_suggestion(cmd)

    def _handle_dashboard(self, args: list[str]) -> str:
        stats = self._state.get_stats()
        birthdays = self._state.address_book_manager.get_dashboard_birthdays()
        return self._renderer.format_dashboard(stats, birthdays)

    def _handle_exit(self, args: list[str]) -> object:
        return EXIT_SENTINEL

    def _handle_help(self, args: list[str]) -> str:
        return self._renderer.format_help()

    def _handle_contacts(self, args: list[str]) -> str:
        normalized = [a.lower() for a in args] if args else []
        match normalized:
            case []:
                return self._contacts_list("")
            case ["add"]:
                return self._contacts_add()
            case ["edit", index_str]:
                return self._contacts_edit(index_str)
            case ["delete", index_str]:
                return self._contacts_delete(index_str)
            case [search_term, *_]:
                return self._contacts_list(args[0])

    def _contacts_list(self, search_term: str) -> str:
        rows = self._state.address_book_manager.get_contacts_table_data(search_term)
        return self._renderer.format_contacts_table(rows)

    def _contacts_add(self) -> str:
        form = ContactConsoleForm()
        data = form.prompt()
        self._state.address_book_manager.add_contact(data)
        # Після додавання показуємо оновлений список
        return self._contacts_list("")

    def _contacts_edit(self, index_str: str) -> str:
        try:
            index = int(index_str)
        except ValueError:
            return "⚠ Індекс має бути числом."

        contacts = self._state.address_book_manager.contacts
        if index < 0 or index >= len(contacts):
            return "⚠ Контакт з таким індексом не знайдено."

        contact = contacts[index]
        existing = contact.to_dict()
        # Використовуємо тільки поля, що підтримує форма
        existing_data = {
            "name": existing.get("name", ""),
            "phone": existing.get("phone", ""),
            "email": existing.get("email", ""),
            "address": existing.get("address", ""),
            "birthday": existing.get("birthday", ""),
        }
        form = ContactConsoleForm(existing=existing_data)
        data = form.prompt()
        self._state.address_book_manager.edit_contact(index, data)
        return self._contacts_list("")

    def _contacts_delete(self, index_str: str) -> str:
        try:
            index = int(index_str)
        except ValueError:
            return "⚠ Індекс має бути числом."

        contacts = self._state.address_book_manager.contacts
        if index < 0 or index >= len(contacts):
            return "⚠ Контакт з таким індексом не знайдено."

        self._state.address_book_manager.delete_contact(index)
        return self._contacts_list("")

    def _handle_notes(self, args: list[str]) -> str:
        normalized = [a.lower() for a in args] if args else []
        match normalized:
            case []:
                return self._notes_list("")
            case ["add"]:
                return self._notes_add()
            case ["edit", index_str]:
                return self._notes_edit(index_str)
            case ["delete", index_str]:
                return self._notes_delete(index_str)
            case [search_term, *_]:
                return self._notes_list(args[0])

    def _notes_list(self, search_term: str) -> str:
        rows = self._state.notes_manager.get_notes_table_data(search_term)
        return self._renderer.format_notes_table(rows)

    def _notes_add(self) -> str:
        form = NoteConsoleForm()
        data = form.prompt()
        self._state.notes_manager.add_note(data)
        return self._notes_list("")

    def _notes_edit(self, index_str: str) -> str:
        try:
            index = int(index_str)
        except ValueError:
            return "⚠ Індекс має бути числом."

        notes = self._state.notes_manager.notes
        if index < 0 or index >= len(notes):
            return "⚠ Нотатку з таким індексом не знайдено."

        note = notes[index]
        existing = note.to_dict()
        existing_data = {
            "text": existing.get("text", ""),
            "tags": existing.get("tags", ""),
        }
        form = NoteConsoleForm(existing=existing_data)
        data = form.prompt()
        self._state.notes_manager.edit_note(index, data)
        return self._notes_list("")

    def _notes_delete(self, index_str: str) -> str:
        try:
            index = int(index_str)
        except ValueError:
            return "⚠ Індекс має бути числом."

        notes = self._state.notes_manager.notes
        if index < 0 or index >= len(notes):
            return "⚠ Нотатку з таким індексом не знайдено."

        self._state.notes_manager.delete_note(index)
        return self._notes_list("")

    def _handle_birthdays(self, args: list[str]) -> str:
        try:
            days = int(args[0]) if args else 7
        except ValueError:
            days = 7
        rows = self._state.address_book_manager.get_birthdays_table_data(days)
        return self._renderer.format_birthdays_table(rows)
