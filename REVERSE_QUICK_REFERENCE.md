# Reverse Conversion - Quick Reference

## One-Liners

```python
# PNG to dict
from json2sprite import png_to_sprite
sprite = png_to_sprite("sprite.png")

# PNG to JSON file
from json2sprite import png_to_json_file
png_to_json_file("sprite.png", "sprite.json")

# Folder conversion
from json2sprite import png_folder_to_json
png_folder_to_json("sprites/", "json/")

# Split spritesheet
from json2sprite import split_spritesheet
split_spritesheet("sheet.png", "out/", 32, 32, padding=4)
```

## CLI Commands

```bash
# Reverse single file
json2sprite --reverse sprite.png

# Reverse folder
json2sprite --reverse sprites/

# Custom pixel size
json2sprite --reverse sprite.png --pixel-size 8

# Forward (unchanged)
json2sprite sprite.json
```

## Common Patterns

### Round-Trip Verification

```python
from json2sprite import process_json_file, png_to_json_file
process_json_file("in.json", "temp.png")
png_to_json_file("temp.png", "out.json", pixel_size=16)
```

### Batch Processing

```python
from pathlib import Path
from json2sprite import png_to_json_file

for png in Path("sprites/").glob("*.png"):
    png_to_json_file(png, f"json/{png.stem}.json")
```

### Sprite Analysis

```python
sprite = png_to_sprite("character.png")
print(f"Size: {len(sprite['grid'][0])}x{len(sprite['grid'])}")
print(f"Colors: {list(sprite['palette'].values())}")
```

## Parameters

| Function | Key Parameters | Defaults |
|----------|---------------|----------|
| `png_to_sprite` | `pixel_size`, `palette_chars` | 16, "A-Z0-9" |
| `png_to_json_file` | `pixel_size`, `pretty` | 16, True |
| `png_folder_to_json` | `pixel_size` | 16 |
| `split_spritesheet` | `sprite_width`, `sprite_height`, `padding` | required, required, 0 |

## Error Handling

```python
try:
    sprite = png_to_sprite("sprite.png", pixel_size=16)
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid image: {e}")
```

## Output Locations

- Forward: `output/`
- Reverse: `output_json/`

## Pixel Size Guide

| Pixel Size | Use Case |
|------------|----------|
| 1 | Already 1:1 sprites |
| 8 | Small retro sprites |
| 16 | Standard pixel art |
| 32 | Large sprites |

## Limitations

- Max 36 colors (by default)
- Dimensions must divide by pixel_size
- Horizontal spritesheets only

## Testing

```bash
pytest tests/test_reverse.py -v
```
