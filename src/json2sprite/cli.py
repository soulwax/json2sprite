# File: src/json2sprite/cli.py

"""Command-line interface for json2sprite."""

import json
import sys
from pathlib import Path

from json2sprite.processor import process_folder, process_json_file


def main() -> None:
    """Main entry point for the CLI."""
    if len(sys.argv) != 2:
        print("Usage: json2sprite <json_file_or_folder>")
        print("\nExamples:")
        print("  json2sprite input/sprite.json")
        print("  json2sprite input/")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_root = Path("output")

    try:
        if input_path.is_file() and input_path.suffix.lower() == ".json":
            output_file = output_root / (input_path.stem + ".png")
            process_json_file(input_path, output_file)
        elif input_path.is_dir():
            process_folder(input_path, output_root)
        else:
            print(f"Error: Invalid input path: {input_path}")
            print("Path must be either a JSON file or a directory")
            sys.exit(1)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
