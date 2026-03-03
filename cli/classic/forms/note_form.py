from cli.classic.colors import Colors

class NoteConsoleForm:
    """Інтерактивна форма введення / редагування нотатки."""

    def __init__(self, existing: dict | None = None) -> None:
        self._existing = existing or {}

    def prompt(self) -> dict:
        print(Colors.title("📝 Текст нотатки (завершіть порожнім рядком або крапкою):"))
        lines: list[str] = []
        while True:
            line = input(Colors.dim("│ "))
            if line.strip() in ("", "."):
                break
            lines.append(line)
        text = "\n".join(lines) if lines else (self._existing.get("text") or "")
        while not text.strip():
            print(Colors.error("  ⚠ Текст обов'язковий."))
            lines = []
            while True:
                line = input(Colors.dim("│ "))
                if line.strip() in ("", "."):
                    break
                lines.append(line)
            text = "\n".join(lines)

        tags_str = input(Colors.accent("🏷 Теги (через кому): ")).strip() or self._existing.get("tags", "")
        return {"text": text, "tags": tags_str}
