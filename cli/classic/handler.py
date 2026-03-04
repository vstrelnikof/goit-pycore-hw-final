import difflib
import inspect
from typing import Callable, final

from cli.classic.forms import ContactConsoleForm, NoteConsoleForm
from cli.classic.renderer import Renderer
from utils.state import AppState


@final
class CommandHandler:
    """Виконує дії за командами: дашборд, контакти, нотатки, дні народження."""

    # Коефіцієнт схожості для fuzzy-збігу підкоманд.
    SUBCMD_CUTOFF = 0.4

    def __init__(self, state: AppState) -> None:
        self._state = state
        self._renderer = Renderer()
        self.contact_actions_map: dict[str, Callable[..., str]] = {
            "add": self._contacts_add,
            "edit": self._contacts_edit,
            "delete": self._contacts_delete,
        }
        self.note_actions_map: dict[str, Callable[..., str]] = {
            "add": self._notes_add,
            "show": self._notes_show,
            "edit": self._notes_edit,
            "delete": self._notes_delete,
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

    def get_subcommand_suggestion(
        self, unknown_sub: str, known: tuple[str, ...]
    ) -> str:
        """Підказка, коли підкоманда не знайдена (немає навіть fuzzy-збігу)."""
        sub = unknown_sub.strip().lower()
        if not sub:
            return (
                "💡 Підкоманди: " + ", ".join(known) + ". Ліміт — число в кінці рядка."
            )
        return (
            "❓ Невідома підкоманда. Введіть одну з: "
            + ", ".join(known)
            + ". Ліміт — число в кінці."
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
        subcommand_map: dict[str, Callable[..., str]],
        list_fn: Callable[[str, int | None], str],
    ) -> str:
        """Диспетчеризація підкоманд за мапером: збіг → виклик методу, інакше список або підказка."""
        normalized = [a.lower() for a in args] if args else []
        if not normalized:
            return list_fn("", None)

        sub, known = normalized[0], tuple(subcommand_map.keys())
        resolved = self._resolve_subcommand(sub, known)

        if resolved is not None and resolved in subcommand_map:
            method = subcommand_map[resolved]
            arg_count = len(inspect.signature(method).parameters)
            if len(normalized) - 1 == arg_count:
                return method(*normalized[1 : 1 + arg_count])

        if len(normalized) == 1 and normalized[0].isdigit() and int(normalized[0]) > 0:
            return list_fn("", int(normalized[0]))

        if resolved is None and sub.strip():
            return self.get_subcommand_suggestion(sub, known)

        search, limit = self.parse_search_and_limit(args)
        return list_fn(search, limit)

    def handle_dashboard(self, args: list[str]) -> str:
        stats = self._state.get_stats()
        birthdays = self._state.address_book_manager.get_dashboard_birthdays()
        return self._renderer.format_dashboard(stats, birthdays)

    def handle_help(self, args: list[str]) -> str:
        return self._renderer.format_help()

    def handle_contacts(self, args: list[str]) -> str:
        return self._handle_subcommands(
            args, self.contact_actions_map, self._contacts_list
        )

    def _contacts_list(self, search_term: str, limit: int | None) -> str:
        return self._list_with_limit(
            self._state.address_book_manager.get_contacts_table_data,
            self._renderer.format_contacts_table,
            search_term,
            limit,
        )

    def _contacts_add(self) -> str:
        form = ContactConsoleForm()
        data = form.prompt()
        self._state.address_book_manager.add_contact(data)
        return self._contacts_list("", None)

    def _contacts_edit(self, index_str: str) -> str:
        contacts = self._state.address_book_manager.contacts
        index, err = self._parse_index(index_str, len(contacts), "Контакт")
        if err is not None:
            return err
        contact = contacts[index]
        existing = contact.to_dict()
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
        return self._contacts_list("", None)

    def _contacts_delete(self, index_str: str) -> str:
        contacts = self._state.address_book_manager.contacts
        index, err = self._parse_index(index_str, len(contacts), "Контакт")
        if err is not None:
            return err
        self._state.address_book_manager.delete_contact(index)
        return self._contacts_list("", None)

    def handle_notes(self, args: list[str]) -> str:
        return self._handle_subcommands(args, self.note_actions_map, self._notes_list)

    def _notes_list(self, search_term: str, limit: int | None) -> str:
        return self._list_with_limit(
            self._state.notes_manager.get_notes_table_data,
            self._renderer.format_notes_table,
            search_term,
            limit,
        )

    def _notes_show(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        return self._renderer.format_note_full(notes[index])

    def _notes_add(self) -> str:
        form = NoteConsoleForm()
        data = form.prompt()
        self._state.notes_manager.add_note(data)
        return self._notes_list("", None)

    def _notes_edit(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        note = notes[index]
        existing = note.to_dict()
        existing_data = {
            "text": existing.get("text", ""),
            "tags": existing.get("tags", ""),
        }
        form = NoteConsoleForm(existing=existing_data)
        data = form.prompt()
        self._state.notes_manager.edit_note(index, data)
        return self._notes_list("", None)

    def _notes_delete(self, index_str: str) -> str:
        notes = self._state.notes_manager.notes
        index, err = self._parse_index(index_str, len(notes), "Нотатку")
        if err is not None:
            return err
        self._state.notes_manager.delete_note(index)
        return self._notes_list("", None)

    def handle_birthdays(self, args: list[str]) -> str:
        try:
            days = int(args[0]) if args else 7
        except ValueError:
            days = 7
        rows = self._state.address_book_manager.get_birthdays_table_data(days)
        return self._renderer.format_birthdays_table(rows)
