# File: src/json2sprite/cli.py

"""Command-line interface for json2sprite."""

import sys
from pathlib import Path
from typing import Tuple

from json2sprite.processor import process_folder, process_json_file
from json2sprite.reverse import png_folder_to_json, png_to_json_file


def print_usage() -> None:
    """Print usage information."""
    print("Usage: json2sprite [--reverse] <input_file_or_folder> [options]")
    print("\nModes:")
    print("  json2sprite input.json              # Convert JSON to PNG")
    print("  json2sprite input/                  # Convert folder of JSON to PNG")
    print("  json2sprite --reverse input.png     # Convert PNG to JSON")
    print("  json2sprite --reverse input/        # Convert folder of PNG to JSON")
    print("\nOptions:")
    print("  --pixel-size N    Pixel size for reverse conversion (default: 16)")
    print("\nExamples:")
    print("  json2sprite input/sprite.json")
    print("  json2sprite input/")
    print("  json2sprite --reverse output/sprite.png")
    print("  json2sprite --reverse output/ --pixel-size 8")


def parse_arguments(args: list) -> Tuple[bool, int, str]:
    """
    Parse command-line arguments.

    Args:
        args: List of command-line arguments

    Returns:
        Tuple of (reverse_mode, pixel_size, input_path)

    Raises:
        SystemExit: If arguments are invalid
    """
    reverse_mode = False
    pixel_size = 16
    input_path_str = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--reverse":
            reverse_mode = True
        elif arg == "--pixel-size":
            if i + 1 >= len(args):
                print("Error: --pixel-size requires a value")
                sys.exit(1)
            try:
                pixel_size = int(args[i + 1])
                if pixel_size < 1:
                    raise ValueError("Pixel size must be positive")
            except ValueError as exc:
                print(f"Error: Invalid pixel size: {exc}")
                sys.exit(1)
            i += 1
        elif arg.startswith("--"):
            print(f"Error: Unknown option: {arg}")
            print_usage()
            sys.exit(1)
        else:
            input_path_str = arg
        i += 1

    if not input_path_str:
        print("Error: No input path specified")
        print_usage()
        sys.exit(1)

    return reverse_mode, pixel_size, input_path_str


def process_reverse_mode(input_path: Path, pixel_size: int) -> None:
    """
    Handle reverse conversion (PNG to JSON).

    Args:
        input_path: Path to input file or folder
        pixel_size: Pixel size for conversion
    """
    output_root = Path("output_json")

    if input_path.is_file() and input_path.suffix.lower() == ".png":
        output_file = output_root / (input_path.stem + ".json")
        png_to_json_file(input_path, output_file, pixel_size=pixel_size)
    elif input_path.is_dir():
        png_folder_to_json(input_path, output_root, pixel_size=pixel_size)
    else:
        print(f"Error: Invalid input path: {input_path}")
        print("Path must be either a PNG file or a directory")
        sys.exit(1)


def process_forward_mode(input_path: Path) -> None:
    """
    Handle forward conversion (JSON to PNG).

    Args:
        input_path: Path to input file or folder
    """
    output_root = Path("output")

    if input_path.is_file() and input_path.suffix.lower() == ".json":
        output_file = output_root / (input_path.stem + ".png")
        process_json_file(input_path, output_file)
    elif input_path.is_dir():
        process_folder(input_path, output_root)
    else:
        print(f"Error: Invalid input path: {input_path}")
        print("Path must be either a JSON file or a directory")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Parse arguments
    reverse_mode, pixel_size, input_path_str = parse_arguments(sys.argv[1:])
    input_path = Path(input_path_str)

    try:
        if reverse_mode:
            process_reverse_mode(input_path, pixel_size)
        else:
            process_forward_mode(input_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except (ValueError, OSError, PermissionError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
