# File: src/json2sprite/__init__.py

"""
json2sprite - Convert JSON sprite descriptions into PNG images and spritesheets.

This package provides utilities to render pixel art sprites defined in JSON format
into PNG images. It supports individual sprites, horizontal spritesheets, and
reverse conversion from PNG back to JSON.
"""

__version__ = "0.5.0"
__author__ = "Soulwax"
__license__ = "AGPL-3.0-or-later"

from json2sprite.core import make_spritesheet, render_sprite
from json2sprite.processor import process_folder, process_json_file
from json2sprite.reverse import (
    png_folder_to_json,
    png_to_json_file,
    png_to_sprite,
    split_spritesheet,
)

__all__ = [
    "render_sprite",
    "make_spritesheet",
    "process_json_file",
    "process_folder",
    "png_to_sprite",
    "png_to_json_file",
    "png_folder_to_json",
    "split_spritesheet",
]
