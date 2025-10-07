# File: src/json2sprite/cli.py

"""Command-line interface for json2sprite."""

import sys
from pathlib import Path
from typing import Optional

from json2sprite.processor import process_folder, process_json_file
from json2sprite.reverse import png_folder_to_json, png_to_json_file, split_spritesheet

__all__ = ["main", "parse_arguments", "CLIConfig"]


def print_usage() -> None:
    """Print usage information."""
    print("Usage: json2sprite [OPTIONS] <input_file_or_folder>")
    print("\nModes:")
    print("  json2sprite input.json              # Convert JSON to PNG")
    print("  json2sprite input/                  # Convert folder of JSON to PNG")
    print("  json2sprite --reverse input.png     # Convert PNG to JSON")
    print("  json2sprite --reverse input/        # Convert folder of PNG to JSON")
    print("\nOptions:")
    print("  --reverse, -r         Reverse mode: PNG to JSON conversion")
    print("  --output, -o PATH     Output directory (default: output/ or output_json/)")
    print("  --pixel-size, -p N    Pixel size for rendering/extraction (default: 16)")
    print("  --padding N           Padding between sprites in sheet (default: 4)")
    print("  --compact             Compact JSON output (no pretty-print)")
    print("  --verbose, -v         Verbose output")
    print("  --quiet, -q           Suppress all output except errors")
    print("  --split               Split spritesheet mode (requires --width and --height)")
    print("  --width N             Sprite width for split mode")
    print("  --height N            Sprite height for split mode")
    print("  --help, -h            Show this help message")
    print("\nExamples:")
    print("  json2sprite input/sprite.json")
    print("  json2sprite -o assets/ input/")
    print("  json2sprite --reverse output/sprite.png -p 8")
    print("  json2sprite --reverse output/ --compact")
    print("  json2sprite --split sheet.png --width 32 --height 32 -o sprites/")
    print("  json2sprite -p 32 --padding 8 input.json")


class CLIConfig:
    """Configuration for CLI execution."""

    def __init__(self):
        self.reverse_mode: bool = False
        self.split_mode: bool = False
        self.pixel_size: int = 16
        self.padding: int = 4
        self.output_path: Optional[Path] = None
        self.input_path: Optional[Path] = None
        self.compact_json: bool = False
        self.verbose: bool = False
        self.quiet: bool = False
        self.sprite_width: Optional[int] = None
        self.sprite_height: Optional[int] = None


def parse_arguments(args: list) -> CLIConfig:
    """
    Parse command-line arguments.

    Args:
        args: List of command-line arguments

    Returns:
        CLIConfig object with parsed settings

    Raises:
        SystemExit: If arguments are invalid
    """
    config = CLIConfig()
    i = 0

    while i < len(args):
        arg = args[i]

        if arg in ("--help", "-h"):
            print_usage()
            sys.exit(0)
        elif arg in ("--reverse", "-r"):
            config.reverse_mode = True
        elif arg == "--split":
            config.split_mode = True
        elif arg in ("--output", "-o"):
            if i + 1 >= len(args):
                print("Error: --output requires a path")
                sys.exit(1)
            config.output_path = Path(args[i + 1])
            i += 1
        elif arg in ("--pixel-size", "-p"):
            if i + 1 >= len(args):
                print("Error: --pixel-size requires a value")
                sys.exit(1)
            try:
                config.pixel_size = int(args[i + 1])
                if config.pixel_size < 1:
                    raise ValueError("Pixel size must be positive")
            except ValueError as exc:
                print(f"Error: Invalid pixel size: {exc}")
                sys.exit(1)
            i += 1
        elif arg == "--padding":
            if i + 1 >= len(args):
                print("Error: --padding requires a value")
                sys.exit(1)
            try:
                config.padding = int(args[i + 1])
                if config.padding < 0:
                    raise ValueError("Padding must be non-negative")
            except ValueError as exc:
                print(f"Error: Invalid padding: {exc}")
                sys.exit(1)
            i += 1
        elif arg == "--width":
            if i + 1 >= len(args):
                print("Error: --width requires a value")
                sys.exit(1)
            try:
                config.sprite_width = int(args[i + 1])
                if config.sprite_width < 1:
                    raise ValueError("Width must be positive")
            except ValueError as exc:
                print(f"Error: Invalid width: {exc}")
                sys.exit(1)
            i += 1
        elif arg == "--height":
            if i + 1 >= len(args):
                print("Error: --height requires a value")
                sys.exit(1)
            try:
                config.sprite_height = int(args[i + 1])
                if config.sprite_height < 1:
                    raise ValueError("Height must be positive")
            except ValueError as exc:
                print(f"Error: Invalid height: {exc}")
                sys.exit(1)
            i += 1
        elif arg == "--compact":
            config.compact_json = True
        elif arg in ("--verbose", "-v"):
            config.verbose = True
        elif arg in ("--quiet", "-q"):
            config.quiet = True
        elif arg.startswith("--"):
            print(f"Error: Unknown option: {arg}")
            print_usage()
            sys.exit(1)
        else:
            config.input_path = Path(arg)
        i += 1

    if config.input_path is None:
        print("Error: No input path specified")
        print_usage()
        sys.exit(1)

    if config.verbose and config.quiet:
        print("Error: Cannot use --verbose and --quiet together")
        sys.exit(1)

    if config.split_mode and (config.sprite_width is None or config.sprite_height is None):
        print("Error: --split requires both --width and --height")
        sys.exit(1)

    return config


def log_output(message: str, config: CLIConfig, force: bool = False) -> None:
    """
    Print message based on verbosity settings.

    Args:
        message: Message to print
        config: CLI configuration
        force: Force output even in quiet mode (for errors)
    """
    if force or (not config.quiet):
        print(message, flush=True)


def process_split_mode(config: CLIConfig) -> None:
    """
    Handle spritesheet splitting mode.

    Args:
        config: CLI configuration
    """
    if config.input_path is None:
        log_output("Error: No input path specified", config, force=True)
        sys.exit(1)

    if not config.input_path.is_file():
        log_output(
            f"Error: Split mode requires a PNG file, got: {config.input_path}", config, force=True
        )
        sys.exit(1)

    if config.output_path is None:
        config.output_path = Path("split_output")

    if config.sprite_width is None or config.sprite_height is None:
        log_output("Error: Split mode requires --width and --height", config, force=True)
        sys.exit(1)

    if config.verbose:
        log_output(f"Splitting spritesheet: {config.input_path}", config)
        log_output(f"Sprite size: {config.sprite_width}x{config.sprite_height}", config)
        log_output(f"Padding: {config.padding}px", config)
        log_output(f"Output: {config.output_path}", config)

    sprites = split_spritesheet(
        config.input_path,
        config.output_path,
        config.sprite_width,
        config.sprite_height,
        padding=config.padding,
        pixel_size=config.pixel_size,
    )

    if not config.quiet:
        log_output(f"✓ Extracted {len(sprites)} sprites to {config.output_path}", config)


def process_reverse_mode(config: CLIConfig) -> None:
    """
    Handle reverse conversion (PNG to JSON).

    Args:
        config: CLI configuration
    """
    if config.input_path is None:
        log_output("Error: No input path specified", config, force=True)
        sys.exit(1)

    if config.output_path is None:
        config.output_path = Path("output_json")

    if config.verbose:
        log_output("Reverse mode: PNG → JSON", config)
        log_output(f"Pixel size: {config.pixel_size}px", config)
        log_output(
            f"Output format: {'compact' if config.compact_json else 'pretty-printed'}", config
        )

    if config.input_path.is_file() and config.input_path.suffix.lower() == ".png":
        output_file = config.output_path / (config.input_path.stem + ".json")
        png_to_json_file(
            config.input_path,
            output_file,
            pixel_size=config.pixel_size,
        )
        if not config.quiet:
            log_output(f"✓ Converted {config.input_path} → {output_file}", config)
    elif config.input_path.is_dir():
        png_folder_to_json(
            config.input_path,
            config.output_path,
            pixel_size=config.pixel_size,
        )
        if not config.quiet:
            log_output(f"✓ Converted folder {config.input_path} → {config.output_path}", config)
        log_output(f"Error: Invalid input path: {config.input_path}", config, force=True)
        log_output("Path must be either a PNG file or a directory", config, force=True)
        sys.exit(1)


def process_forward_mode(config: CLIConfig) -> None:
    """
    Handle forward conversion (JSON to PNG).

    Args:
        config: CLI configuration
    """
    if config.input_path is None:
        log_output("Error: No input path specified", config, force=True)
        sys.exit(1)

    if config.output_path is None:
        config.output_path = Path("output")

    if config.verbose:
        log_output("Forward mode: JSON → PNG", config)
        log_output(f"Pixel size: {config.pixel_size}px", config)
        log_output(f"Padding: {config.padding}px", config)

    if config.input_path.is_file() and config.input_path.suffix.lower() == ".json":
        output_file = config.output_path / (config.input_path.stem + ".png")
        process_json_file(
            config.input_path,
            output_file,
            pixel_size=config.pixel_size,
            padding=config.padding,
        )
        if not config.quiet:
            log_output(f"✓ Converted {config.input_path} → {output_file}", config)
    elif config.input_path.is_dir():
        process_folder(
            config.input_path,
            config.output_path,
            pixel_size=config.pixel_size,
            padding=config.padding,
        )
        if not config.quiet:
            log_output(f"✓ Converted folder {config.input_path} → {config.output_path}", config)
    else:
        log_output(f"Error: Invalid input path: {config.input_path}", config, force=True)
        log_output("Path must be either a JSON file or a directory", config, force=True)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    try:
        config = parse_arguments(sys.argv[1:])

        if config.split_mode:
            process_split_mode(config)
        elif config.reverse_mode:
            process_reverse_mode(config)
        else:
            process_forward_mode(config)

    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, OSError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
