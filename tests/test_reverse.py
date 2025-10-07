# File: tests/test_reverse.py

"""Tests for reverse conversion (PNG to JSON)."""

import json
from pathlib import Path

import pytest
from PIL import Image

from json2sprite.core import render_sprite
from json2sprite.reverse import (
    png_folder_to_json,
    png_to_json_file,
    png_to_sprite,
    split_spritesheet,
)


@pytest.fixture
def simple_sprite_data():
    """Fixture providing simple sprite data."""
    return {
        "grid": ["RR", "RR"],
        "palette": {"R": "#FF0000"},
    }


@pytest.fixture
def simple_png(tmp_path, simple_sprite_data):
    """Fixture creating a simple PNG file."""
    png_file = tmp_path / "test.png"
    img = render_sprite(simple_sprite_data, pixel_size=16)
    img.save(png_file)
    return png_file


class TestPngToSprite:
    """Tests for png_to_sprite function."""

    def test_simple_conversion(self, simple_png):
        """Test converting a simple PNG to sprite data."""
        result = png_to_sprite(simple_png, pixel_size=16)

        assert "grid" in result
        assert "palette" in result
        assert "sprite_name" in result
        assert len(result["grid"]) == 2
        assert len(result["grid"][0]) == 2

    def test_preserves_colors(self, simple_png):
        """Test that colors are preserved in conversion."""
        result = png_to_sprite(simple_png, pixel_size=16)

        # Should have red color
        has_red = any("#FF0000" in str(v) for v in result["palette"].values())
        assert has_red

    def test_handles_transparency(self, tmp_path):
        """Test handling of transparent pixels."""
        sprite = {
            "grid": [".R.", "RRR", ".R."],
            "palette": {".": "transparent", "R": "#00FF00"},
        }
        png_file = tmp_path / "transparent.png"
        img = render_sprite(sprite, pixel_size=8)
        img.save(png_file)

        result = png_to_sprite(png_file, pixel_size=8)

        assert "." in result["palette"]
        assert result["palette"]["."] == "transparent"

    def test_file_not_found(self, tmp_path):
        """Test error when PNG file doesn't exist."""
        non_existent = tmp_path / "nonexistent.png"

        with pytest.raises(FileNotFoundError):
            png_to_sprite(non_existent)

    def test_invalid_dimensions(self, tmp_path):
        """Test error when dimensions aren't divisible by pixel_size."""
        png_file = tmp_path / "invalid.png"
        # Create 33x33 image (not divisible by 16)
        img = Image.new("RGBA", (33, 33), (255, 0, 0, 255))
        img.save(png_file)

        with pytest.raises(ValueError, match="divisible by pixel_size"):
            png_to_sprite(png_file, pixel_size=16)

    def test_custom_pixel_size(self, tmp_path):
        """Test with custom pixel size."""
        sprite = {"grid": ["RR"], "palette": {"R": "#0000FF"}}
        png_file = tmp_path / "custom.png"
        img = render_sprite(sprite, pixel_size=8)
        img.save(png_file)

        result = png_to_sprite(png_file, pixel_size=8)

        assert len(result["grid"]) == 1
        assert len(result["grid"][0]) == 2

    def test_sprite_name_from_filename(self, tmp_path):
        """Test that sprite name is derived from filename."""
        sprite = {"grid": ["R"], "palette": {"R": "#FF0000"}}
        png_file = tmp_path / "my_sprite.png"
        img = render_sprite(sprite, pixel_size=16)
        img.save(png_file)

        result = png_to_sprite(png_file, pixel_size=16)

        assert result["sprite_name"] == "my_sprite"


class TestPngToJsonFile:
    """Tests for png_to_json_file function."""

    def test_creates_json_file(self, simple_png, tmp_path):
        """Test that JSON file is created."""
        output_file = tmp_path / "output.json"

        png_to_json_file(simple_png, output_file)

        assert output_file.exists()

    def test_json_is_valid(self, simple_png, tmp_path):
        """Test that output is valid JSON."""
        output_file = tmp_path / "output.json"

        png_to_json_file(simple_png, output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 1
        assert "grid" in data[0]
        assert "palette" in data[0]

    def test_creates_output_directory(self, simple_png, tmp_path):
        """Test that output directory is created if needed."""
        output_file = tmp_path / "nested" / "dirs" / "output.json"

        png_to_json_file(simple_png, output_file)

        assert output_file.exists()
        assert output_file.parent.exists()

    def test_pretty_print(self, simple_png, tmp_path):
        """Test pretty-printed JSON output."""
        output_file = tmp_path / "pretty.json"

        png_to_json_file(simple_png, output_file, pretty=True)

        content = output_file.read_text()
        # Pretty-printed JSON should have newlines and indentation
        assert "\n" in content
        assert "  " in content

    def test_compact_output(self, simple_png, tmp_path):
        """Test compact JSON output."""
        output_file = tmp_path / "compact.json"

        png_to_json_file(simple_png, output_file, pretty=False)

        # Compact should be shorter than pretty
        compact_size = output_file.stat().st_size

        output_file2 = tmp_path / "pretty.json"
        png_to_json_file(simple_png, output_file2, pretty=True)
        pretty_size = output_file2.stat().st_size

        assert compact_size < pretty_size


class TestPngFolderToJson:
    """Tests for png_folder_to_json function."""

    def test_processes_folder(self, tmp_path, simple_sprite_data):
        """Test processing a folder of PNG files."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        # Create test PNG files
        for i in range(3):
            png_file = input_folder / f"sprite{i}.png"
            img = render_sprite(simple_sprite_data, pixel_size=16)
            img.save(png_file)

        png_folder_to_json(input_folder, output_folder)

        assert (output_folder / "sprite0.json").exists()
        assert (output_folder / "sprite1.json").exists()
        assert (output_folder / "sprite2.json").exists()

    def test_maintains_directory_structure(self, tmp_path, simple_sprite_data):
        """Test that directory structure is preserved."""
        input_folder = tmp_path / "input"
        nested = input_folder / "nested"
        nested.mkdir(parents=True)
        output_folder = tmp_path / "output"

        png1 = input_folder / "root.png"
        png2 = nested / "nested.png"

        img = render_sprite(simple_sprite_data, pixel_size=16)
        img.save(png1)
        img.save(png2)

        png_folder_to_json(input_folder, output_folder)

        assert (output_folder / "root.json").exists()
        assert (output_folder / "nested" / "nested.json").exists()

    def test_skips_non_png_files(self, tmp_path, simple_sprite_data):
        """Test that non-PNG files are skipped."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        # Create PNG and non-PNG files
        png_file = input_folder / "sprite.png"
        img = render_sprite(simple_sprite_data, pixel_size=16)
        img.save(png_file)

        (input_folder / "readme.txt").write_text("Not a PNG")
        (input_folder / "data.json").write_text("{}")

        png_folder_to_json(input_folder, output_folder)

        assert (output_folder / "sprite.json").exists()
        assert not (output_folder / "readme.json").exists()
        assert not (output_folder / "data.json").exists()

    def test_folder_not_found(self, tmp_path):
        """Test error when input folder doesn't exist."""
        non_existent = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError):
            png_folder_to_json(non_existent, tmp_path / "output")

    def test_empty_folder(self, tmp_path, capsys):
        """Test processing an empty folder."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        png_folder_to_json(input_folder, output_folder)

        captured = capsys.readouterr()
        assert "No PNG files found" in captured.out


class TestSplitSpritesheet:
    """Tests for split_spritesheet function."""

    def test_splits_horizontal_sheet(self, tmp_path, simple_sprite_data):
        """Test splitting a horizontal spritesheet."""
        from json2sprite.core import make_spritesheet

        # Create a spritesheet with 3 sprites
        sprites = [simple_sprite_data] * 3
        sheet = make_spritesheet(sprites, pixel_size=16, padding=4)

        sheet_path = tmp_path / "sheet.png"
        sheet.save(sheet_path)
        output_folder = tmp_path / "split"

        result = split_spritesheet(
            sheet_path, output_folder, sprite_width=32, sprite_height=32, padding=4, pixel_size=16
        )

        assert len(result) == 3
        assert (output_folder / "sprite_000.json").exists()
        assert (output_folder / "sprite_001.json").exists()
        assert (output_folder / "sprite_002.json").exists()

    def test_sheet_not_found(self, tmp_path):
        """Test error when spritesheet doesn't exist."""
        non_existent = tmp_path / "nonexistent.png"

        with pytest.raises(FileNotFoundError):
            split_spritesheet(non_existent, tmp_path / "output", 32, 32)

    def test_invalid_sprite_height(self, tmp_path):
        """Test error when sprite height exceeds sheet height."""
        # Create small sheet
        img = Image.new("RGBA", (32, 16), (255, 0, 0, 255))
        sheet_path = tmp_path / "sheet.png"
        img.save(sheet_path)

        with pytest.raises(ValueError, match="exceeds sheet height"):
            split_spritesheet(sheet_path, tmp_path / "output", 32, 64)

    def test_sprite_names_include_index(self, tmp_path, simple_sprite_data):
        """Test that sprite names include index."""
        from json2sprite.core import make_spritesheet

        sprites = [simple_sprite_data] * 2
        sheet = make_spritesheet(sprites, pixel_size=16, padding=0)

        sheet_path = tmp_path / "mysheet.png"
        sheet.save(sheet_path)
        output_folder = tmp_path / "split"

        result = split_spritesheet(
            sheet_path, output_folder, sprite_width=32, sprite_height=32, padding=0, pixel_size=16
        )

        assert "mysheet_sprite_0" in result[0]["sprite_name"]
        assert "mysheet_sprite_1" in result[1]["sprite_name"]
