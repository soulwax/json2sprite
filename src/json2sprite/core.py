"""Core sprite rendering functionality."""

from typing import Dict, List, Tuple

from PIL import Image


def render_sprite(sprite: Dict, pixel_size: int = 16) -> Image.Image:
    """
    Render a single sprite from JSON data to a PIL Image.

    Args:
        sprite: Dictionary containing 'grid' and 'palette' keys
        pixel_size: Size of each pixel in the output image (default: 16)

    Returns:
        PIL Image object with RGBA mode

    Raises:
        KeyError: If required keys are missing from sprite data
        ValueError: If grid or palette data is invalid
    """
    if "grid" not in sprite:
        raise KeyError("Sprite data missing 'grid' key")
    if "palette" not in sprite:
        raise KeyError("Sprite data missing 'palette' key")

    grid = sprite["grid"]
    palette = sprite["palette"]

    if not grid or not isinstance(grid, list):
        raise ValueError("Grid must be a non-empty list")

    height = len(grid)
    width = len(grid[0]) if grid else 0

    if not all(len(row) == width for row in grid):
        raise ValueError("All rows in grid must have the same length")

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            color = palette.get(char, "transparent")
            if color == "transparent":
                continue

            if not isinstance(color, str) or not color.startswith("#"):
                raise ValueError(f"Invalid color format: {color}")

            try:
                rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
                img.putpixel((x, y), rgb + (255,))
            except (ValueError, IndexError) as exc:
                raise ValueError(f"Invalid hex color: {color}") from exc

    return img.resize((width * pixel_size, height * pixel_size), Image.NEAREST)


def make_spritesheet(sprites: List[Dict], pixel_size: int = 16, padding: int = 4) -> Image.Image:
    """
    Create a horizontal spritesheet from multiple sprites.

    Args:
        sprites: List of sprite dictionaries
        pixel_size: Size of each pixel in the output (default: 16)
        padding: Pixels between sprites (default: 4)

    Returns:
        PIL Image object containing the spritesheet

    Raises:
        ValueError: If sprites list is empty
    """
    if not sprites:
        raise ValueError("Cannot create spritesheet from empty sprite list")

    rendered = [render_sprite(s, pixel_size) for s in sprites]
    widths, heights = zip(*(im.size for im in rendered))

    total_width = sum(widths) + padding * (len(rendered) - 1)
    max_height = max(heights)

    sheet = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_offset = 0
    for img in rendered:
        sheet.paste(img, (x_offset, 0), img)
        x_offset += img.width + padding

    return sheet
