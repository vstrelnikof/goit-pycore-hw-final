from models.table_row import TableData, TableRow


def test_table_row_to_tuple_returns_cells_and_index() -> None:
    row = TableRow(cells=["a", "b"], index=0)
    assert row.to_tuple() == (["a", "b"], 0)


def test_table_data_is_list_of_table_row() -> None:
    data: TableData = [
        TableRow(cells=["x"], index=0),
        TableRow(cells=["y"], index=1),
    ]
    assert len(data) == 2
    assert data[0].cells == ["x"] and data[0].index == 0
    assert data[1].cells == ["y"] and data[1].index == 1
