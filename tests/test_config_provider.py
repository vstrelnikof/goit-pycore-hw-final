import logging
from pathlib import Path
import pytest
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider

def test_load_uses_defaults_when_config_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["pytest"])  # щоб argparse не отримав pytest-аргументи

    app_config: AppConfig = ConfigProvider.load()

    assert isinstance(app_config, AppConfig)
    assert app_config.log_level == logging.INFO


def test_load_reads_config_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["pytest"])
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n"
        "  log_level: 10\n"
        "  theme: \"green\"\n"
        "  app_data_paths:\n"
        "    address_book: data/ab.json\n"
        "    notes: data/notes.json\n",
        encoding="utf-8",
    )

    app_config: AppConfig = ConfigProvider.load(config_path)

    assert app_config.log_level == 10
    path_str = str(app_config.app_data_paths.address_book)
    assert path_str.replace("\\", "/").endswith("data/ab.json")


def test_load_classic_true_when_arg_passed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  log_level: 20\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["main.py", "--classic"])
    app_config = ConfigProvider.load(config_path)
    assert app_config.classic is True


def test_load_classic_from_config_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  log_level: 20\n  classic: true\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["pytest"])
    app_config = ConfigProvider.load(config_path)
    assert app_config.classic is True

