# test_compact.py - run this first
from pathlib import Path

from json2sprite import render_sprite
from json2sprite.reverse import png_to_json_file

sprite = {"grid": ["R"], "palette": {"R": "#FF0000"}}
img = render_sprite(sprite, pixel_size=16)

img.save("test.png")
png_to_json_file("test.png", "compact.json", pretty=False)
png_to_json_file("test.png", "pretty.json", pretty=True)

compact = Path("compact.json").read_text()
pretty = Path("pretty.json").read_text()

print(f"Compact ({len(compact)} chars):\n{compact}\n")
print(f"Pretty ({len(pretty)} chars):\n{pretty}\n")
print(f"Test passes: {len(compact) < len(pretty)}")