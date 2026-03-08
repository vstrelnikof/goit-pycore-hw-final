from collections import namedtuple
import difflib
import inspect
from typing import Callable, final

from cli.classic.forms import ContactConsoleForm, FormCancelledError, NoteConsoleForm
from cli.classic.renderer import CommandRenderer
from utils.state import AppState

ActionHandler = namedtuple("SubcommandHandler", ["usage_hint", "handler"])


@final
class CommandHandler:
    """Виконує дії за командами: дашборд, контакти, нотатки, дні народження."""

    # Коефіцієнт схожості для fuzzy-збігу підкоманд.
    SUBCMD_CUTOFF = 0.1
    CANCEL_MESSAGE = "✗ Дію скасовано."

    def __init__(self, state: AppState) -> None:
        self._state = state
        self._renderer = CommandRenderer()
        self.contact_handlers: dict[str, ActionHandler] = {
            "add": ActionHandler("add", self._contacts_add),
            "edit": ActionHandler("edit <індекс>", self._contacts_edit),
            "delete": ActionHandler("delete <індекс>", self._contacts_delete),
            "search": ActionHandler("search [пошук] [N]", self._contacts_search),
        }
        self.note_handlers: dict[str, ActionHandler] = {
            "add": ActionHandler("add", self._notes_add),
            "show": ActionHandler("show <індекс>", self._notes_show),
            "edit": ActionHandler("edit <індекс>", self._notes_edit),
            "delete": ActionHandler("delete <індекс>", self._notes_delete),
            "search": ActionHandler("search [пошук] [N]", self._notes_search),
        }

    @staticmethod
    def _resolve_subcommand(word: str, known: tuple[str, ...]) -> str | None:
        """Повертає точний або єдиний fuzzy-збіг підкоманди, інакше None."""
        w = word.strip().lower()
        if not w:
            return None
        if w in known:
            return w
        matches = difflib.get_close_matches(
            w, list(known), n=1, cutoff=CommandHandler.SUBCMD_CUTOFF
        )
        return matches[0] if matches else None

    @staticmethod
    def _parse_index(
        index_str: str, upper_bound: int, entity: str
    ) -> tuple[int | None, str | None]:
        """Повертає (index, None) або (None, повідомлення про помилку)."""
        try:
            index = int(index_str)
        except ValueError:
            return None, "⚠ Індекс має бути числом."
        if index < 0 or index >= upper_bound:
            return None, f"⚠ {entity} з таким індексом не знайдено."
        return index, None

    @staticmethod
    def _confirm_delete(entity_name: str) -> bool:
        """Підтвердження видалення: питає користувача (y/n), повертає True лише для y/yes."""
        try:
            reply = (
                input(f"Ви впевнені, що хочете видалити {entity_name}? (y/n): ")
                .strip()
                .lower()
            )
        except (EOFError, KeyboardInterrupt):
            return False
        return reply in ("y", "yes", "так")

    def get_subcommand_suggestion(
        self,
        unknown_sub: str,
        known: tuple[str, ...],
        *,  # Всі наступні keyword-only
        usage_map: dict[str, str] | None = None,
    ) -> str:
        """Підказка, коли підкоманда не знайдена (немає навіть fuzzy-збігу)."""
        parts = [(usage_map or {}).get(k, k) for k in known]
        parts_str = ", ".join(parts)
        if not unknown_sub.strip():
            return f"💡 Підкоманди: {parts_str}."
        return f"❓ Невідома підкоманда. Введіть одну з: {parts_str}."

    def get_subcommand_params_hint(
        self,
        resolved: str,
        expected_count: int,
        actual_count: int,
        context_name: str,
        usage_map: dict[str, str],
    ) -> str:
        """Підказка, коли підкоманда вірна, але параметрів не вистачає або зайво."""
        usage = usage_map.get(resolved, resolved)
        prefix = f"{context_name} " if context_name else ""
        if expected_count == 0:
            return (
                f"💡 Підкоманда '{resolved}' не потребує параметрів. "
                f"Приклад: {prefix}{resolved}"
            )
        if actual_count < expected_count:
            need = "індекс (число)" if "індекс" in usage else "параметри"
            return (
                f"💡 Підкоманда '{resolved}' потребує параметр: {need}. "
                f"Приклад: {prefix}{usage}"
            )
        return (
            f"💡 Підкоманда '{resolved}' приймає лише {expected_count} параметр(и). "
            f"Використання: {prefix}{usage}"
        )

    @staticmethod
    def parse_search_and_limit(args: list[str]) -> tuple[str, int | None]:
        """Парсить аргументи списку: останній якщо число — ліміт рядків, решта — пошук."""
        if not args:
            return "", None
        if len(args) == 1:
            if args[0].isdigit() and int(args[0]) > 0:
                return "", int(args[0])
            return args[0], None
        if args[-1].isdigit() and int(args[-1]) > 0:
            return " ".join(args[:-1]).strip(), int(args[-1])
        return " ".join(args), None

    def _list_with_limit(
        self,
        get_rows: Callable[[str], list],
        format_table: Callable[..., str],
        search_term: str,
        limit: int | None,
    ) -> str:
        """Спільна логіка: отримати рядки, обрізати по limit, відформатувати з total_count при потребі."""
        rows = get_rows(search_term)
        if limit is not None and limit > 0 and len(rows) > limit:
            total = len(rows)
            rows = rows[:limit]
            return format_table(rows, total_count=total)
        return format_table(rows)

    def _handle_subcommands(
        self,
        args: list[str],
        handlers: dict[str, ActionHandler],
        list_fn: Callable[[str, int | None], str],
        *,
        context_name: str = "",
    ) -> str:
        """Обробка підкоманд: збіг → виклик обробника, інакше підказка. Пошук лише через підкоманду search."""
        normalized = [a.lower() for a in args] if args else []
        known = tuple(handlers.keys())
        subcommand_map = {k: v.handler for k, v in handlers.items()}
        usage_map = {k: v.usage_hint for k, v in handlers.items()}

        if not normalized:
            return self.get_subcommand_suggestion("", known, usage_map=usage_map)

        sub = normalized[0]
        resolved = self._resolve_subcommand(sub, known)

        if resolved == "search":
            search, limit = self.parse_search_and_limit(args[1:])
            return list_fn(search, limit)

        if resolved is not None and resolved in subcommand_map:
            method = subcommand_map[resolved]
            arg_count = len(inspect.signature(method).parameters)
            given_count = len(normalized) - 1
            if given_count == arg_count:
                return method(*normalized[1 : 1 + arg_count])
            return self.get_subcommand_params_hint(
                resolved, arg_count, given_count, context_name, usage_map
            )

        return self.get_subcommand_suggestion(sub, known, usage_map=usage_map)

    def handle_dashboard(self, args: list[str]) -> str:
        stats = self._state.get_stats()
        birthdays = self._state.address_book_manager.get_dashboard_birthdays()
        return self._renderer.format_dashboard(stats, birthdays)

    def handle_help(self, args: list[str]) -> str:
        return self._renderer.format_help()

    def handle_contacts(self, args: list[str]) -> str:
        return self._handle_subcommands(
            args,
            self.contact_handlers,
            self._contacts_list,
            context_name="contacts",
        )

    def _contacts_list(self, search_term: str, limit: int | None = None) -> str:
        return self._list_with_limit(
            self._state.address_book_manager.get_contacts_table_data,
            self._renderer.format_contacts_table,
            search_term,
            limit,
        )

    def _contacts_search(self, *args: str) -> str:
        search, limit = self.parse_search_and_limit(list(args))
        return self._contacts_list(search, limit)

    def _contacts_add(self) -> str:
        form = ContactConsoleForm()
        try:
            data = form.prompt()
        except FormCancelledError:
            return CommandHandler.CANCEL_MESSAGE
        self._state.address_book_manager.add_contact(data)
        return self._contacts_list("")

    def _contacts_edit(self, index_str: str) -> str:
        contacts = self._state.address_book_manager.contacts
        index, err = self._parse_index(index_str, len(contacts), "Контакт")
        if err is not None:
            return err
        form = ContactConsoleForm(existing=contacts[index].to_dict())
        try:
            data = form.prompt()
        except FormCancelledError:
            return CommandHandler.CANCEL_MESSAGE
        self._state.address_book_manager.edit_contact(index, data)
        return self._contacts_list("")

    def _contacts_delete(self, index_str: str) -> str:
        contacts = self._state.address_book_manager.contacts
        index, err = self._parse_index(index_str, len(contacts), "Контакт")
        if err is not None:
            return err
        if not self._confirm_delete("контакт"):
            return CommandHandler.CANCEL_MESSAGE
        self._state.address_book_manager.delete_contact(index)
        return self._contacts_list("")

    def handle_notes(self, args: list[str]) -> str:
        return self._handle_subcommands(
            args,
            self.note_handlers,
            self._notes_list,
            context_name="notes",
        )

    def _notes_list(self, search_term: str, limit: int | None) -> str:
        return self._list_with_limit(
            self._state.notes_manager.get_notes_table_data,
            self._renderer.format_notes_table,
            search_term,
            limit,
        )

    def _notes_search(self, *args: str) -> str:
        search, limit = self.parse_search_and_limit(list(args))
        return self._notes_list(search, limit)

    def _notes_show(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        return self._renderer.format_note_full(notes[index])

    def _notes_add(self) -> str:
        form = NoteConsoleForm()
        try:
            data = form.prompt()
        except FormCancelledError:
            return CommandHandler.CANCEL_MESSAGE
        self._state.notes_manager.add_note(data)
        return self._notes_list("", None)

    def _notes_edit(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        form = NoteConsoleForm(
            existing={"text": notes[index].text, "tags": notes[index].tags_string}
        )
        try:
            data = form.prompt()
        except FormCancelledError:
            return CommandHandler.CANCEL_MESSAGE
        self._state.notes_manager.edit_note(index, data)
        return self._notes_list("", None)

    def _notes_delete(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        if not self._confirm_delete("нотатку"):
            return CommandHandler.CANCEL_MESSAGE
        self._state.notes_manager.delete_note(index)
        return self._notes_list("", None)

    def handle_birthdays(self, args: list[str]) -> str:
        try:
            days = int(args[0]) if args else 7
        except ValueError:
            days = 7
        rows = self._state.address_book_manager.get_birthdays_table_data(days)
        return self._renderer.format_birthdays_table(rows)
