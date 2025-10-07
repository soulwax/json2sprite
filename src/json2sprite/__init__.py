"""
json2sprite - Convert JSON sprite descriptions into PNG images and spritesheets.

This package provides utilities to render pixel art sprites defined in JSON format
into PNG images. It supports individual sprites and horizontal spritesheets.
"""

__version__ = "0.1.0"
__author__ = "Soulwax"
__license__ = "AGPL-3.0-or-later"

from json2sprite.core import make_spritesheet, render_sprite
from json2sprite.processor import process_folder, process_json_file

__all__ = [
    "render_sprite",
    "make_spritesheet",
    "process_json_file",
    "process_folder",
]
