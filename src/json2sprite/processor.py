"""File processing utilities for JSON to sprite conversion."""

import json
import os
from pathlib import Path
from typing import Union

from json2sprite.core import make_spritesheet


def process_json_file(json_path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """
    Process a single JSON file and save the resulting sprite/spritesheet.

    Args:
        json_path: Path to input JSON file
        output_path: Path for output PNG file

    Raises:
        FileNotFoundError: If input file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON structure is invalid
    """
    json_path = Path(json_path)
    output_path = Path(output_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Input file not found: {json_path}")

    print(f"Processing {json_path} -> {output_path}", flush=True)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of sprite objects")

    sheet = make_spritesheet(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)

    print(f"Saved {output_path}", flush=True)


def process_folder(input_folder: Union[str, Path], output_folder: Union[str, Path]) -> None:
    """
    Process all JSON files in a folder, maintaining directory structure.

    Args:
        input_folder: Path to input folder
        output_folder: Path to output folder

    Raises:
        FileNotFoundError: If input folder doesn't exist
    """
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    if not input_folder.is_dir():
        raise ValueError(f"Input path is not a directory: {input_folder}")

    json_files_found = False

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".json"):
                json_files_found = True
                json_path = Path(root) / file
                relative_path = json_path.relative_to(input_folder).with_suffix(".png")
                output_path = output_folder / relative_path

                try:
                    process_json_file(json_path, output_path)
                except Exception as exc:
                    print(f"Error processing {json_path}: {exc}", flush=True)

    if not json_files_found:
        print(f"No JSON files found in {input_folder}", flush=True)
