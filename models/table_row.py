from __future__ import annotations
from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=False)
class TableRow:
    """Один рядок таблиці: комірки для колонок та ідентифікатор запису (для edit/delete)."""

    cells: list[str]
    id: str

    def to_tuple(self) -> tuple[list[str], str]:
        """Повертає (cells, id) для сумісності з віджетами (наприклад MultiColumnListBox)."""
        return (self.cells, self.id)


# Тип для списку рядків таблиці (контакти, нотатки, дні народження тощо)
TableData = list[TableRow]
