import logging
from pathlib import Path
import pytest
from models.app_config import AppConfig
from providers.config_provider import ConfigProvider


def test_load_uses_defaults_when_config_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv", ["pytest"]
    )  # щоб argparse не отримав pytest-аргументи

    app_config: AppConfig = ConfigProvider.load()

    assert isinstance(app_config, AppConfig)
    assert app_config.log_level == logging.INFO


def test_load_reads_config_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["pytest"])
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n"
        "  log_level: 10\n"
        '  theme: "green"\n'
        "  app_data_paths:\n"
        "    address_book: data/ab.json\n"
        "    notes: data/notes.json\n",
        encoding="utf-8",
    )

    app_config: AppConfig = ConfigProvider.load(config_path)

    assert app_config.log_level == 10
    path_str = str(app_config.app_data_paths.address_book)
    assert path_str.replace("\\", "/").endswith("data/ab.json")


def test_load_classic_true_when_arg_passed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  log_level: 20\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["main.py", "--classic"])
    app_config = ConfigProvider.load(config_path)
    assert app_config.classic is True


def test_load_classic_from_config_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  log_level: 20\n  classic: true\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["pytest"])
    app_config = ConfigProvider.load(config_path)
    assert app_config.classic is True


def test_load_create_fakes_from_args(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  log_level: 20\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "--create-fakes-contacts", "3", "--create-fakes-notes", "5"],
    )
    app_config = ConfigProvider.load(config_path)
    assert app_config.create_fakes_contacts == 3
    assert app_config.create_fakes_notes == 5


def test_create_fakes_default_zero_when_no_args(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app:\n  app_data_paths:\n    address_book: data/c.json\n    notes: data/n.json\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["pytest"])
    app_config = ConfigProvider.load(config_path)
    assert app_config.create_fakes_contacts == 0
    assert app_config.create_fakes_notes == 0


def test_load_uses_profile_config_when_cli_config_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--config <profile> має вибирати config.<profile>.yaml поруч із базовим файлом."""
    monkeypatch.chdir(tmp_path)
    base_config_path = tmp_path / "config.yaml"
    base_config_path.write_text(
        "app:\n"
        "  log_level: 20\n"
        "  app_data_paths:\n"
        "    address_book: data/base.json\n"
        "    notes: data/base_notes.json\n",
        encoding="utf-8",
    )
    profile_config_path = tmp_path / "config.test.yaml"
    profile_config_path.write_text(
        "app:\n"
        "  log_level: 10\n"
        "  app_data_paths:\n"
        "    address_book: data/test.json\n"
        "    notes: data/test_notes.json\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["main.py", "--config", "test"])
    app_config = ConfigProvider.load(base_config_path)

    assert app_config.log_level == 10
    path_str = str(app_config.app_data_paths.address_book)
    assert path_str.replace("\\", "/").endswith("data/test.json")


def test_load_uses_explicit_config_path_from_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--config <path> має використовувати явний шлях до файлу конфігурації."""
    monkeypatch.chdir(tmp_path)
    # Базовий файл, який не повинен бути використаний
    base_config_path = tmp_path / "config.yaml"
    base_config_path.write_text(
        "app:\n"
        "  log_level: 20\n"
        "  app_data_paths:\n"
        "    address_book: data/base.json\n"
        "    notes: data/base_notes.json\n",
        encoding="utf-8",
    )
    explicit_config_path = tmp_path / "custom_config.yaml"
    explicit_config_path.write_text(
        "app:\n"
        "  log_level: 30\n"
        "  app_data_paths:\n"
        "    address_book: data/custom.json\n"
        "    notes: data/custom_notes.json\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["main.py", "--config", str(explicit_config_path)])
    app_config = ConfigProvider.load()

    assert app_config.log_level == 30
    path_str = str(app_config.app_data_paths.address_book)
    assert path_str.replace("\\", "/").endswith("data/custom.json")
