from pathlib import Path
from providers.storage_provider import StorageProvider


def test_storage_provider_initializes_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "data.json"

    storage = StorageProvider(file_path)

    # Файл має бути створений
    assert file_path.exists()
    assert list(storage.load_list()) == []


def test_storage_provider_saves_and_loads_list(tmp_path: Path) -> None:
    file_path = tmp_path / "data.json"
    storage = StorageProvider(file_path)
    data = [{"id": 1, "value": "test"}, {"id": 2, "value": "demo"}]

    storage.save(data)

    loaded = list(storage.load_list())
    assert loaded == data

