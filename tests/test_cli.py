# File: tests/test_cli.py

"""Tests for CLI functionality."""

import json
import sys
from pathlib import Path

import pytest

from json2sprite.cli import main, parse_arguments
from json2sprite.core import render_sprite


@pytest.fixture
def valid_sprite_data():
    """Fixture providing valid sprite data."""
    return [{"grid": ["R"], "palette": {"R": "#FF0000"}}]


class TestParseArguments:
    """Tests for argument parsing."""

    def test_parse_basic_input(self):
        """Test parsing basic input path."""
        config = parse_arguments(["input.json"])
        assert config.input_path == Path("input.json")
        assert not config.reverse_mode
        assert config.pixel_size == 16
        assert config.padding == 4

    def test_parse_reverse_flag(self):
        """Test parsing reverse flag."""
        config = parse_arguments(["--reverse", "input.png"])
        assert config.reverse_mode
        assert config.input_path == Path("input.png")

    def test_parse_short_reverse_flag(self):
        """Test parsing short reverse flag."""
        config = parse_arguments(["-r", "input.png"])
        assert config.reverse_mode

    def test_parse_output_path(self):
        """Test parsing output path."""
        config = parse_arguments(["-o", "custom_output/", "input.json"])
        assert config.output_path == Path("custom_output/")

    def test_parse_pixel_size(self):
        """Test parsing pixel size."""
        config = parse_arguments(["-p", "32", "input.json"])
        assert config.pixel_size == 32

    def test_parse_padding(self):
        """Test parsing padding."""
        config = parse_arguments(["--padding", "8", "input.json"])
        assert config.padding == 8

    def test_parse_compact_flag(self):
        """Test parsing compact flag."""
        config = parse_arguments(["--compact", "input.json"])
        assert config.compact_json

    def test_parse_verbose_flag(self):
        """Test parsing verbose flag."""
        config = parse_arguments(["-v", "input.json"])
        assert config.verbose

    def test_parse_quiet_flag(self):
        """Test parsing quiet flag."""
        config = parse_arguments(["-q", "input.json"])
        assert config.quiet

    def test_parse_split_mode(self):
        """Test parsing split mode."""
        config = parse_arguments(["--split", "--width", "32", "--height", "32", "sheet.png"])
        assert config.split_mode
        assert config.sprite_width == 32
        assert config.sprite_height == 32

    def test_parse_multiple_flags(self):
        """Test parsing multiple flags together."""
        config = parse_arguments(["-r", "-p", "8", "-o", "out/", "--compact", "input.png"])
        assert config.reverse_mode
        assert config.pixel_size == 8
        assert config.output_path == Path("out/")
        assert config.compact_json

    def test_invalid_pixel_size(self, monkeypatch, capsys):
        """Test error with invalid pixel size."""
        with pytest.raises(SystemExit):
            parse_arguments(["-p", "invalid", "input.json"])

    def test_negative_pixel_size(self, monkeypatch, capsys):
        """Test error with negative pixel size."""
        with pytest.raises(SystemExit):
            parse_arguments(["-p", "-1", "input.json"])

    def test_missing_output_value(self):
        """Test error when output flag has no value."""
        with pytest.raises(SystemExit):
            parse_arguments(["-o"])

    def test_verbose_and_quiet_conflict(self):
        """Test error when both verbose and quiet are specified."""
        with pytest.raises(SystemExit):
            parse_arguments(["-v", "-q", "input.json"])

    def test_split_without_dimensions(self):
        """Test error when split mode lacks dimensions."""
        with pytest.raises(SystemExit):
            parse_arguments(["--split", "sheet.png"])

    def test_help_flag(self, monkeypatch):
        """Test help flag exits cleanly."""
        with pytest.raises(SystemExit) as exc_info:
            parse_arguments(["--help"])
        assert exc_info.value.code == 0


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
        monkeypatch.setattr(sys, "argv", ["json2sprite", "--help"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Examples:" in captured.out
        assert "--reverse" in captured.out
        assert "--split" in captured.out

    def test_process_json_file(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test processing a single JSON file via CLI."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        assert (tmp_path / "output" / "test.png").exists()

    def test_process_with_custom_output(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test processing with custom output directory."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        output_dir = tmp_path / "custom_out"
        monkeypatch.setattr(sys, "argv", ["json2sprite", "-o", str(output_dir), str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        assert (output_dir / "test.png").exists()

    def test_process_with_custom_pixel_size(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test processing with custom pixel size."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        monkeypatch.setattr(sys, "argv", ["json2sprite", "-p", "32", str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        output_file = tmp_path / "output" / "test.png"
        assert output_file.exists()
        from PIL import Image

        img = Image.open(output_file)
        assert img.size == (32, 32)

    def test_reverse_mode(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test reverse mode via CLI."""
        sprite = valid_sprite_data[0]
        img = render_sprite(sprite, pixel_size=16)
        png_file = tmp_path / "test.png"
        img.save(png_file)

        monkeypatch.setattr(sys, "argv", ["json2sprite", "--reverse", str(png_file)])
        monkeypatch.chdir(tmp_path)

        main()

        assert (tmp_path / "output_json" / "test.json").exists()

    # ! MAJOR TODO: Do not ignore this test - implement compact mode in reverse.py to pass it, not just
    # ! to "just work" in real life scenarios, even though that's what matters for now.
    @pytest.mark.xfail(reason="Compact mode implementation pending")
    def test_reverse_compact_mode(self, monkeypatch, tmp_path, valid_sprite_data):
        """Test reverse mode with compact JSON."""
        sprite = valid_sprite_data[0]
        img = render_sprite(sprite, pixel_size=16)
        png_file = tmp_path / "test.png"
        img.save(png_file)

        monkeypatch.setattr(sys, "argv", ["json2sprite", "-r", "--compact", str(png_file)])
        monkeypatch.chdir(tmp_path)

        main()

        json_file = tmp_path / "output_json" / "test.json"
        assert json_file.exists()

        # Compact JSON should be significantly smaller than pretty-printed
        content = json_file.read_text()

        # Re-parse to verify it's valid JSON
        data = json.loads(content)
        assert isinstance(data, list)

        # Pretty-print version for comparison
        pretty_version = json.dumps(data, indent=2)

        # Compact should be smaller (no indentation/extra whitespace)
        assert len(content) < len(pretty_version)

    def test_verbose_mode(self, monkeypatch, tmp_path, valid_sprite_data, capsys):
        """Test verbose output."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        monkeypatch.setattr(sys, "argv", ["json2sprite", "-v", str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        captured = capsys.readouterr()
        assert "Forward mode" in captured.out or "JSON → PNG" in captured.out

    def test_quiet_mode(self, monkeypatch, tmp_path, valid_sprite_data, capsys):
        """Test quiet mode suppresses output."""
        input_file = tmp_path / "test.json"
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(valid_sprite_data, f)

        monkeypatch.setattr(sys, "argv", ["json2sprite", "-q", str(input_file)])
        monkeypatch.chdir(tmp_path)

        main()

        captured = capsys.readouterr()
        assert "✓" not in captured.out

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

    def test_keyboard_interrupt(self, monkeypatch, tmp_path):
        """Test handling of keyboard interrupt."""
        input_file = tmp_path / "test.json"
        input_file.write_text("[]")

        def mock_process(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr(sys, "argv", ["json2sprite", str(input_file)])
        monkeypatch.setattr("json2sprite.cli.process_forward_mode", mock_process)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 130
