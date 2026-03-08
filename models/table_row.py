from __future__ import annotations
from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=False)
class TableRow:
    """Один рядок таблиці: комірки для колонок та індекс запису (для edit/delete)."""

    cells: list[str]
    index: int

    def to_tuple(self) -> tuple[list[str], int]:
        """Повертає (cells, index) для сумісності з віджетами (наприклад MultiColumnListBox)."""
        return (self.cells, self.index)


# Тип для списку рядків таблиці (контакти, нотатки, дні народження тощо)
TableData = list[TableRow]
