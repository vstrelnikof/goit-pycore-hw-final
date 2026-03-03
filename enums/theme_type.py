from enum import StrEnum
from typing import final


@final
class ThemeType(StrEnum):
    """Доступні для використання теми asciimatics"""

    DEFAULT = "default"
    MONOCHROME = "monochrome"
    GREEN = "green"
    BRIGHT = "bright"
