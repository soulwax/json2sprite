# File: src/json2sprite/reverse.py

"""Reverse conversion: PNG images to JSON sprite format."""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

from PIL import Image


def _extract_color_from_pixel(pixel_value) -> Tuple[int, int, int, int]:
    """
    Normalize pixel value to RGBA tuple.

    Args:
        pixel_value: Pixel value from image

    Returns:
        RGBA tuple (r, g, b, a)
    """
    if not isinstance(pixel_value, tuple):
        return (pixel_value, pixel_value, pixel_value, 255)
    if len(pixel_value) == 3:
        return pixel_value + (255,)
    return pixel_value


def _assign_palette_char(
    color: Tuple[int, int, int, int],
    color_map: Dict,
    palette_chars: str,
    char_index: int,
) -> Tuple[str, int]:
    """
    Assign a character to a color in the palette.

    Args:
        color: RGBA color tuple
        color_map: Current color to character mapping
        palette_chars: Available characters for palette
        char_index: Current character index

    Returns:
        Tuple of (character, new_char_index)

    Raises:
        ValueError: If too many unique colors
    """
    if color in color_map:
        return color_map[color], char_index

    if char_index >= len(palette_chars):
        raise ValueError(
            f"Too many unique colors (>{len(palette_chars)}). "
            "Increase palette_chars or reduce image colors."
        )

    char = palette_chars[char_index]
    color_map[color] = char
    return char, char_index + 1


def _process_grid_cell(
    img: Image.Image,
    x: int,
    y: int,
    pixel_size: int,
    *,
    color_map: Dict,
    palette_chars: str,
    char_index: int,
) -> Tuple[str, int]:
    """
    Process a single grid cell and return its character.

    Args:
        img: PIL Image object
        x: Grid X coordinate
        y: Grid Y coordinate
        pixel_size: Size of each pixel
        color_map: Current color to character mapping
        palette_chars: Available palette characters
        char_index: Current character index

    Returns:
        Tuple of (character, new_char_index)
    """
    # Sample the center pixel of each grid cell
    sample_x = x * pixel_size + pixel_size // 2
    sample_y = y * pixel_size + pixel_size // 2
    pixel = img.getpixel((sample_x, sample_y))

    color = _extract_color_from_pixel(pixel)

    # Handle transparent pixels
    if color[3] == 0:
        return ".", char_index

    char, char_index = _assign_palette_char(color, color_map, palette_chars, char_index)
    return char, char_index


def _build_grid_from_image(
    img: Image.Image,
    grid_width: int,
    grid_height: int,
    pixel_size: int,
    palette_chars: str,
) -> Tuple[List[str], Dict[Tuple[int, int, int, int], str]]:
    """
    Build grid and color map from image.

    Args:
        img: PIL Image object
        grid_width: Grid width in cells
        grid_height: Grid height in cells
        pixel_size: Size of each pixel
        palette_chars: Characters for palette

    Returns:
        Tuple of (grid, color_map)

    Raises:
        ValueError: If too many colors
    """
    color_map: Dict[Tuple[int, int, int, int], str] = {(0, 0, 0, 0): "."}
    grid: List[str] = []
    char_index = 0

    for y in range(grid_height):
        row = []
        for x in range(grid_width):
            char, char_index = _process_grid_cell(
                img,
                x,
                y,
                pixel_size,
                color_map=color_map,
                palette_chars=palette_chars,
                char_index=char_index,
            )
            row.append(char)

        grid.append("".join(row))

    return grid, color_map


def _build_palette_from_colors(color_map: Dict[Tuple[int, int, int, int], str]) -> Dict[str, str]:
    """
    Build palette dictionary from color map.

    Args:
        color_map: Mapping of colors to characters

    Returns:
        Palette dictionary
    """
    palette: Dict[str, str] = {}
    for color, char in color_map.items():
        if color == (0, 0, 0, 0):
            palette[char] = "transparent"
        else:
            # Convert RGBA to hex
            hex_color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
            palette[char] = hex_color
    return palette


def png_to_sprite(
    image_path: Union[str, Path],
    pixel_size: int = 16,
    palette_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
) -> Dict:
    """
    Convert a PNG image to sprite JSON format.

    Args:
        image_path: Path to input PNG file
        pixel_size: Size of each pixel in the original sprite (default: 16)
        palette_chars: Characters to use for palette keys (default: A-Z, 0-9)

    Returns:
        Dictionary with 'grid' and 'palette' keys

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image dimensions aren't divisible by pixel_size
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    if width % pixel_size != 0 or height % pixel_size != 0:
        raise ValueError(
            f"Image dimensions ({width}x{height}) must be divisible by pixel_size ({pixel_size})"
        )

    grid_width = width // pixel_size
    grid_height = height // pixel_size

    # Build grid and extract colors
    grid, color_map = _build_grid_from_image(
        img, grid_width, grid_height, pixel_size, palette_chars
    )

    # Build palette from colors
    palette = _build_palette_from_colors(color_map)

    return {
        "sprite_name": image_path.stem,
        "grid": grid,
        "palette": palette,
    }


def png_to_json_file(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    pixel_size: int = 16,
    pretty: bool = True,
) -> None:
    """
    Convert a PNG file to JSON and save it.

    Args:
        image_path: Path to input PNG file
        output_path: Path for output JSON file
        pixel_size: Size of each pixel in the original sprite (default: 16)
        pretty: Use pretty-printed JSON (default: True)

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image is invalid
    """
    image_path = Path(image_path)
    output_path = Path(output_path)

    print(f"Converting {image_path} -> {output_path}", flush=True)

    sprite = png_to_sprite(image_path, pixel_size=pixel_size)

    # Wrap in list for compatibility with json2sprite format
    data = [sprite]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    print(f"Saved {output_path}", flush=True)


def png_folder_to_json(
    input_folder: Union[str, Path],
    output_folder: Union[str, Path],
    pixel_size: int = 16,
) -> None:
    """
    Convert all PNG files in a folder to JSON, maintaining directory structure.

    Args:
        input_folder: Path to input folder with PNG files
        output_folder: Path to output folder for JSON files
        pixel_size: Size of each pixel in the original sprites (default: 16)

    Raises:
        FileNotFoundError: If input folder doesn't exist
    """
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    if not input_folder.is_dir():
        raise ValueError(f"Input path is not a directory: {input_folder}")

    png_files_found = False

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".png"):
                png_files_found = True
                png_path = Path(root) / file
                relative_path = png_path.relative_to(input_folder).with_suffix(".json")
                output_path = output_folder / relative_path

                try:
                    png_to_json_file(png_path, output_path, pixel_size=pixel_size)
                except (FileNotFoundError, ValueError, OSError, PermissionError) as exc:
                    print(f"Error processing {png_path}: {exc}", flush=True)

    if not png_files_found:
        print(f"No PNG files found in {input_folder}", flush=True)


def _extract_sprite_from_sheet(
    sheet: Image.Image,
    x_offset: int,
    sprite_width: int,
    sprite_height: int,
) -> Image.Image:
    """
    Extract a single sprite from a spritesheet.

    Args:
        sheet: The spritesheet image
        x_offset: X offset to start extraction
        sprite_width: Width of sprite to extract
        sprite_height: Height of sprite to extract

    Returns:
        Extracted sprite image
    """
    return sheet.crop((x_offset, 0, x_offset + sprite_width, sprite_height))


def _save_sprite_json(
    sprite_data: Dict,
    output_folder: Path,
    sprite_index: int,
) -> None:
    """
    Save sprite data to JSON file.

    Args:
        sprite_data: Sprite dictionary
        output_folder: Output folder path
        sprite_index: Index of the sprite
    """
    json_path = output_folder / f"sprite_{sprite_index:03d}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([sprite_data], f, indent=2, ensure_ascii=False)
    print(f"Extracted sprite {sprite_index} -> {json_path}", flush=True)


def split_spritesheet(
    sheet_path: Union[str, Path],
    output_folder: Union[str, Path],
    sprite_width: int,
    sprite_height: int,
    *,
    padding: int = 0,
    pixel_size: int = 16,
) -> List[Dict]:
    """
    Split a horizontal spritesheet into individual sprites.

    Args:
        sheet_path: Path to spritesheet PNG file
        output_folder: Folder to save individual sprite JSONs
        sprite_width: Width of each sprite in pixels
        sprite_height: Height of each sprite in pixels
        padding: Padding between sprites in pixels (default: 0)
        pixel_size: Pixel size for conversion (default: 16)

    Returns:
        List of sprite dictionaries

    Raises:
        FileNotFoundError: If sheet file doesn't exist
        ValueError: If dimensions are invalid
    """
    sheet_path = Path(sheet_path)
    output_folder = Path(output_folder)

    if not sheet_path.exists():
        raise FileNotFoundError(f"Spritesheet not found: {sheet_path}")

    sheet = Image.open(sheet_path).convert("RGBA")
    sheet_width, sheet_height = sheet.size

    if sprite_height > sheet_height:
        raise ValueError(f"Sprite height ({sprite_height}) exceeds sheet height ({sheet_height})")

    sprites = []
    x_offset = 0
    sprite_index = 0

    output_folder.mkdir(parents=True, exist_ok=True)

    while x_offset + sprite_width <= sheet_width:
        # Extract sprite from sheet
        sprite_img = _extract_sprite_from_sheet(sheet, x_offset, sprite_width, sprite_height)

        # Save temporarily to convert
        temp_path = output_folder / f"sprite_{sprite_index:03d}.png"
        sprite_img.save(temp_path)

        # Convert to JSON format
        sprite_data = png_to_sprite(temp_path, pixel_size=pixel_size)
        sprite_data["sprite_name"] = f"{sheet_path.stem}_sprite_{sprite_index}"
        sprites.append(sprite_data)

        # Save individual JSON
        _save_sprite_json(sprite_data, output_folder, sprite_index)

        x_offset += sprite_width + padding
        sprite_index += 1

    print(f"Extracted {sprite_index} sprites from {sheet_path}", flush=True)

    return sprites
