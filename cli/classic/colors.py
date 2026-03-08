from __future__ import annotations


class Colors:
    """Утилітарний клас для стилізації тексту ANSI-кодами."""

    # ANSI escape
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Кольори (8-bit 256: м'які тони)
    CYAN = "\033[38;5;37m"  # заголовки, інфо
    GREEN = "\033[38;5;34m"  # успіх
    YELLOW = "\033[38;5;220m"  # підказки, дати
    MAGENTA = "\033[38;5;129m"  # акцент (напр. команди)
    RED = "\033[38;5;203m"  # помилки, попередження
    GRAY = "\033[38;5;245m"  # роздільники, другорядний текст

    @staticmethod
    def dim(text: str) -> str:
        """Повертає рядок у приглушеному (dim) стилі для другорядного тексту."""
        return f"{Colors.DIM}{text}{Colors.RESET}"

    @staticmethod
    def title(text: str) -> str:
        """Повертає рядок як заголовок: жирний циановий текст."""
        return f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}"

    @staticmethod
    def success(text: str) -> str:
        """Повертає рядок зеленим кольором для повідомлень про успіх."""
        return f"{Colors.GREEN}{text}{Colors.RESET}"

    @staticmethod
    def hint(text: str) -> str:
        """Повертає рядок жовтим кольором для підказок та підсвічування."""
        return f"{Colors.YELLOW}{text}{Colors.RESET}"

    @staticmethod
    def accent(text: str) -> str:
        """Повертає рядок акцентним (пурпурним) кольором, напр. для промпту чи команд."""
        return f"{Colors.MAGENTA}{text}{Colors.RESET}"

    @staticmethod
    def error(text: str) -> str:
        """Повертає рядок червоним кольором для помилок та попереджень."""
        return f"{Colors.RED}{text}{Colors.RESET}"

    @staticmethod
    def separator(text: str) -> str:
        """Повертає рядок сірим кольором для роздільників та другорядного тексту."""
        return f"{Colors.GRAY}{text}{Colors.RESET}"
