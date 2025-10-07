# File: tests/test_processor.py

"""Tests for file processing functionality."""

import json
from pathlib import Path

import pytest

from json2sprite.processor import process_folder, process_json_file


@pytest.fixture
def valid_sprite_data():
    """Fixture providing valid sprite data."""
    return [
        {
            "grid": ["RR", "RR"],
            "palette": {"R": "#FF0000"},
        }
    ]


@pytest.fixture
def temp_json_file(tmp_path, valid_sprite_data):
    """Fixture creating a temporary JSON file."""
    json_file = tmp_path / "test.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(valid_sprite_data, f)
    return json_file


class TestProcessJsonFile:
    """Tests for process_json_file function."""

    def test_process_valid_file(self, temp_json_file, tmp_path):
        """Test processing a valid JSON file."""
        output_file = tmp_path / "output" / "test.png"

        process_json_file(temp_json_file, output_file)

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_file_not_found(self, tmp_path):
        """Test error when input file doesn't exist."""
        non_existent = tmp_path / "nonexistent.json"
        output = tmp_path / "output.png"

        with pytest.raises(FileNotFoundError):
            process_json_file(non_existent, output)

    def test_invalid_json(self, tmp_path):
        """Test error with invalid JSON."""
        invalid_json = tmp_path / "invalid.json"
        with open(invalid_json, "w", encoding="utf-8") as f:
            f.write("not valid json{")

        with pytest.raises(json.JSONDecodeError):
            process_json_file(invalid_json, tmp_path / "output.png")

    def test_non_list_json(self, tmp_path):
        """Test error when JSON root is not a list."""
        non_list_json = tmp_path / "nonlist.json"
        with open(non_list_json, "w", encoding="utf-8") as f:
            json.dump({"not": "a list"}, f)

        with pytest.raises(ValueError, match="must be a list"):
            process_json_file(non_list_json, tmp_path / "output.png")

    def test_output_directory_creation(self, temp_json_file, tmp_path):
        """Test that output directories are created automatically."""
        output_file = tmp_path / "nested" / "dirs" / "output.png"

        process_json_file(temp_json_file, output_file)

        assert output_file.exists()
        assert output_file.parent.exists()

    def test_process_with_pathlib_path(self, temp_json_file, tmp_path):
        """Test processing with pathlib.Path objects."""
        output_file = tmp_path / "output.png"

        process_json_file(Path(temp_json_file), Path(output_file))

        assert output_file.exists()

    def test_process_with_string_path(self, temp_json_file, tmp_path):
        """Test processing with string paths."""
        output_file = tmp_path / "output.png"

        process_json_file(str(temp_json_file), str(output_file))

        assert output_file.exists()


class TestProcessFolder:
    """Tests for process_folder function."""

    def test_process_empty_folder(self, tmp_path, capsys):
        """Test processing a folder with no JSON files."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        process_folder(input_folder, output_folder)

        captured = capsys.readouterr()
        assert "No JSON files found" in captured.out

    def test_process_folder_with_files(self, tmp_path, valid_sprite_data):
        """Test processing a folder with JSON files."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        # Create test JSON files
        (input_folder / "sprite1.json").write_text(json.dumps(valid_sprite_data))
        (input_folder / "sprite2.json").write_text(json.dumps(valid_sprite_data))

        process_folder(input_folder, output_folder)

        assert (output_folder / "sprite1.png").exists()
        assert (output_folder / "sprite2.png").exists()

    def test_process_nested_folders(self, tmp_path, valid_sprite_data):
        """Test processing nested folder structure."""
        input_folder = tmp_path / "input"
        nested_folder = input_folder / "nested"
        nested_folder.mkdir(parents=True)
        output_folder = tmp_path / "output"

        (input_folder / "root.json").write_text(json.dumps(valid_sprite_data))
        (nested_folder / "nested.json").write_text(json.dumps(valid_sprite_data))

        process_folder(input_folder, output_folder)

        assert (output_folder / "root.png").exists()
        assert (output_folder / "nested" / "nested.png").exists()

    def test_folder_not_found(self, tmp_path):
        """Test error when input folder doesn't exist."""
        non_existent = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError):
            process_folder(non_existent, tmp_path / "output")

    def test_input_path_not_directory(self, tmp_path):
        """Test error when input path is not a directory."""
        not_a_dir = tmp_path / "file.txt"
        not_a_dir.write_text("content")

        with pytest.raises(ValueError, match="not a directory"):
            process_folder(not_a_dir, tmp_path / "output")

    def test_skip_non_json_files(self, tmp_path, valid_sprite_data):
        """Test that non-JSON files are skipped."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        (input_folder / "sprite.json").write_text(json.dumps(valid_sprite_data))
        (input_folder / "readme.txt").write_text("Not a JSON file")
        (input_folder / "data.xml").write_text("<xml/>")

        process_folder(input_folder, output_folder)

        assert (output_folder / "sprite.png").exists()
        assert not (output_folder / "readme.png").exists()
        assert not (output_folder / "data.png").exists()

    def test_error_handling_continues_processing(self, tmp_path, valid_sprite_data, capsys):
        """Test that errors in one file don't stop processing others."""
        input_folder = tmp_path / "input"
        input_folder.mkdir()
        output_folder = tmp_path / "output"

        # One valid, one invalid
        (input_folder / "valid.json").write_text(json.dumps(valid_sprite_data))
        (input_folder / "invalid.json").write_text("invalid json{")

        process_folder(input_folder, output_folder)

        captured = capsys.readouterr()
        assert "Error processing" in captured.out
        # Valid file should still be processed
        assert (output_folder / "valid.png").exists()
