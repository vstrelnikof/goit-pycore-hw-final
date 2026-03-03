from typing import Literal
from models.table_row import TableData, TableRow
from cli.classic.colors import Colors

Align = Literal["<", ">"]

class Renderer:
    """Форматування виводу команд: таблиці з колонками заданої ширини та вирівнювання."""

    _SEP = "  "

    @staticmethod
    def _cell(value: str, width: int, align: Align = "<") -> str:
        """Одна комірка: обрізає по width і форматує через f\"{text:{align}{width}}\"."""
        s = str(value)
        if len(s) > width:
            s = s[: max(0, width - 2)] + ".."
        return f"{s:{align}{width}}"

    def _format_table(
        self,
        rows: TableData,
        col_widths: list[int],
        titles: list[str],
        aligns: list[Align],
        show_index: bool = False,
    ) -> list[str]:
        """Загальна таблиця: заголовок, роздільник, рядки. show_index — перша колонка індекс."""
        lines = []
        # Заголовок
        if show_index:
            header_cells = [self._cell(titles[0], col_widths[0], aligns[0])]
            header_cells += [
                self._cell(t, col_widths[i + 1], aligns[i + 1])
                for i, t in enumerate(titles[1:])
            ]
        else:
            header_cells = [
                self._cell(t, col_widths[i], aligns[i]) for i, t in enumerate(titles)
            ]
        lines.append(Colors.title(self._SEP.join(header_cells)))
        total_width = sum(col_widths) + len(self._SEP) * (len(col_widths) - 1)
        lines.append(Colors.separator("-" * total_width))
        # Рядки
        for row in rows:
            row_cells, index = row.cells, row.index
            if show_index:
                cells = [self._cell(str(index), col_widths[0], aligns[0])]
                cells += [
                    self._cell(c, col_widths[i + 1], aligns[i + 1])
                    for i, c in enumerate(row_cells)
                ]
            else:
                cells = [
                    self._cell(c, col_widths[i], aligns[i])
                    for i, c in enumerate(row_cells)
                ]
            lines.append(self._SEP.join(cells))
        return lines

    def format_contacts_table(self, rows: TableData) -> str:
        """Таблиця контактів з індексом для edit/delete."""
        if not rows:
            return Colors.dim("📭 Контактів не знайдено.")
        col_widths = [4, 25, 18, 22, 20, 12]
        titles = ["", "👤 Ім'я", "📞 Телефон", "✉ Email", "📍 Адреса", "🎂 Дата"]
        aligns: list[Align] = [">", "<", "<", "<", "<", "<"]
        return "\n".join(
            self._format_table(rows, col_widths, titles, aligns, show_index=True)
        )

    def format_notes_table(self, rows: TableData) -> str:
        """Таблиця нотаток з індексом."""
        if not rows:
            return Colors.dim("📝 Нотаток не знайдено.")
        width_text = 55
        width_tags = 30
        col_widths = [4, width_text, width_tags]
        titles = ["", "📝 Зміст", "🏷 Теги"]
        aligns: list[Align] = [">", "<", "<"]
        truncated_rows: TableData = [
            TableRow(
                cells=[
                    row.cells[0][: width_text - 2] + ".." if len(row.cells[0]) > width_text else row.cells[0],
                    row.cells[1],
                ],
                index=row.index,
            )
            for row in rows
        ]
        return "\n".join(
            self._format_table(truncated_rows, col_widths, titles, aligns, show_index=True)
        )

    def format_birthdays_table(self, rows: TableData) -> str:
        """Таблиця днів народження."""
        if not rows:
            return Colors.dim("🎂 На вказаний період іменинників немає.")
        col_widths = [12, 20, 18, 22, 20]
        titles = ["🎂 Дата", "👤 Ім'я", "📞 Телефон", "✉ Email", "📍 Адреса"]
        aligns: list[Align] = [">", "<", "<", "<", "<"]
        return "\n".join(
            self._format_table(rows, col_widths, titles, aligns, show_index=False)
        )
