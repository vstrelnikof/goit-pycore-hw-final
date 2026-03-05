from cli.classic.colors import Colors
from cli.classic.forms.base_form import ConsoleFormBase


class NoteConsoleForm(ConsoleFormBase):
    """Інтерактивна форма введення / редагування нотатки."""

    def _prompt_text(self) -> str:
        print(Colors.title("📝 Текст нотатки (завершіть порожнім рядком або крапкою):"))
        existing_text: str = self._existing.get("text") or ""
        if existing_text.strip():
            print(Colors.dim("Поточний текст (залиште порожнім, щоб не змінювати):"))
            for line in existing_text.splitlines():
                print(Colors.dim(f"│ {line}"))
            print(Colors.dim("─" * 40))

        lines: list[str] = []
        while True:
            line = self._read_line_or_raise()
            if line.strip() in ("", "."):
                break
            lines.append(line)
        text = "\n".join(lines) if lines else existing_text
        while not text.strip():
            print(Colors.error("  ⚠ Текст обов'язковий."))
            lines = []
            while True:
                line = self._read_line_or_raise()
                if line.strip() in ("", "."):
                    break
                lines.append(line)
            text = "\n".join(lines)
        return text

    def _prompt_tags(self) -> str:
        existing = self._existing.get("tags", "")
        prompt = (
            "🏷 Теги (через кому): "
            if not existing
            else f"🏷 Теги (через кому) {existing}: "
        )
        return self._read_field(prompt, existing)

    def prompt(self) -> dict:
        self._print_cancel_hint()
        return {
            "text": self._prompt_text(),
            "tags": self._prompt_tags(),
        }
