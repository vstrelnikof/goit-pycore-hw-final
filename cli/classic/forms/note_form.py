from cli.classic.colors import Colors


class NoteConsoleForm:
    """Інтерактивна форма введення / редагування нотатки."""

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def prompt(self) -> dict:
        print(Colors.title("📝 Текст нотатки (завершіть порожнім рядком або крапкою):"))
        existing_text: str = self._existing.get("text") or ""
        if existing_text.strip():
            print(Colors.dim("Поточний текст (залиште порожнім, щоб не змінювати):"))
            for line in existing_text.splitlines():
                print(Colors.dim(f"│ {line}"))
            print(Colors.dim("─" * 40))

        lines: list[str] = []
        while True:
            line = input(Colors.dim("│ "))
            if line.strip() in ("", "."):
                break
            lines.append(line)
        text = "\n".join(lines) if lines else existing_text
        while not text.strip():
            print(Colors.error("  ⚠ Текст обов'язковий."))
            lines = []
            while True:
                line = input(Colors.dim("│ "))
                if line.strip() in ("", "."):
                    break
                lines.append(line)
            text = "\n".join(lines)

        existing_tags = self._existing.get("tags", "")
        tags_prompt = (
            "🏷 Теги (через кому): "
            if not existing_tags
            else f"🏷 Теги (через кому) [{existing_tags}]: "
        )
        tags_str = input(Colors.accent(tags_prompt)).strip() or existing_tags
        return {"text": text, "tags": tags_str}
