from models.table_row import TableData, TableRow


def test_table_row_to_tuple_returns_cells_and_id() -> None:
    row = TableRow(cells=["a", "b"], id="abc-123")
    assert row.to_tuple() == (["a", "b"], "abc-123")


def test_table_data_is_list_of_table_row() -> None:
    data: TableData = [
        TableRow(cells=["x"], id="id-0"),
        TableRow(cells=["y"], id="id-1"),
    ]
    assert len(data) == 2
    assert data[0].cells == ["x"] and data[0].id == "id-0"
    assert data[1].cells == ["y"] and data[1].id == "id-1"
