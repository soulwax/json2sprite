# File: tests/test_cli.py

"""Tests for CLI functionality."""

import json
import sys
from pathlib import Path

import pytest

from json2sprite.cli import main


@pytest.fixture
def valid_sprite_data():
    """Fixture providing valid sprite data."""
    return [{"grid": ["R"], "palette": {"R": "#FF0000"}}]


class TestCLI:
    """Tests for command-line interface."""

    def test_no_arguments(self, monkeypatch, capsys):
        """Test CLI with no arguments."""
        monkeypatch.setattr(sys, "argv", ["json2sprite"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_help_message(self, monkeypatch, capsys):
        """Test that help message shows examples."""
        monkeypatch.setattr(sys, "argv", ["json2sprite"])

        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Examples:" in captured.out

    def test_process_json_file(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test processing a single JSON file via CLI."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        assert (tmp_path / "output" / "test.png").exists()

    def test_process_folder(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test processing a folder via CLI."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        (input_folder / "sprite.json").write_text(json.dumps(valid_sprite_data))

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(input_folder)])
        monkeypatch.chdir(tmp_path)

        main()

        assert (tmp_path / "output" / "sprite.png").exists()

    def test_invalid_input_path(self, monkeypatch, tmp_path, capsys):
        """Test error with invalid input path."""
        non_existent = tmp_path / "nonexistent.json"

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(non_existent)])
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_non_json_file(self, monkeypatch, tmp_path, capsys):
        """Test error when file is not JSON."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("not json")

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(text_file)])
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Invalid input path" in captured.out
