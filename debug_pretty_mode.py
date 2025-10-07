# Quick debug test - run this to check if compact works
import json
import tempfile
from pathlib import Path

from json2sprite import png_to_json_file, render_sprite

# Create test sprite
sprite = {"grid": ["R"], "palette": {"R": "#FF0000"}}
img = render_sprite(sprite, pixel_size=16)

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    # Save PNG
    png_file = tmp_path / "test.png"
    img.save(png_file)

    # Test compact mode
    json_compact = tmp_path / "compact.json"
    png_to_json_file(png_file, json_compact, pixel_size=16, pretty=False)

    # Test pretty mode
    json_pretty = tmp_path / "pretty.json"
    png_to_json_file(png_file, json_pretty, pixel_size=16, pretty=True)

    # Compare
    compact_content = json_compact.read_text()
    pretty_content = json_pretty.read_text()

    print(f"Compact length: {len(compact_content)}")
    print(f"Pretty length: {len(pretty_content)}")
    print(f"\nCompact content:\n{compact_content}")
    print(f"\nPretty content:\n{pretty_content}")
    print(f"\nCompact is smaller: {len(compact_content) < len(pretty_content)}")
