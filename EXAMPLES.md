# Usage Examples

This document provides comprehensive examples of using json2sprite for both forward (JSON to PNG) and reverse (PNG to JSON) conversions.

## Forward Conversion: JSON to PNG

### Example 1: Simple Sprite

**Input JSON** (`input/heart.json`):

```json
[
  {
    "sprite_name": "heart",
    "grid": [
      ".##.##.",
      "#####",
      "#####",
      ".###.",
      "..#.."
    ],
    "palette": {
      ".": "transparent",
      "#": "#FF0000"
    }
  }
]
```

**Command:**

```bash
json2sprite input/heart.json
```

**Output:** `output/heart.png` - A red heart sprite

### Example 2: Multiple Sprites (Spritesheet)

**Input JSON** (`input/characters.json`):

```json
[
  {
    "sprite_name": "player",
    "grid": [
      "..H..",
      ".HHH.",
      "..H..",
      ".H.H.",
      "H...H"
    ],
    "palette": {
      ".": "transparent",
      "H": "#00FFFF"
    }
  },
  {
    "sprite_name": "enemy",
    "grid": [
      "..E..",
      ".EEE.",
      "E.E.E",
      ".EEE.",
      "..E.."
    ],
    "palette": {
      ".": "transparent",
      "E": "#FF00FF"
    }
  }
]
```

**Command:**

```bash
json2sprite input/characters.json
```

**Output:** `output/characters.png` - Horizontal spritesheet with both characters

### Example 3: Complex Palette

**Input JSON** (`input/flag.json`):

```json
[
  {
    "sprite_name": "flag",
    "grid": [
      "BRRRRRRR",
      "RWWWWWWW",
      "BRRRRRRR",
      "RWWWWWWW",
      "BRRRRRRR",
      "RWWWWWWW",
      "BRRRRRRR",
      "P.......P",
      "P.......P"
    ],
    "palette": {
      ".": "transparent",
      "R": "#FF0000",
      "W": "#FFFFFF",
      "B": "#0000FF",
      "P": "#8B4513"
    }
  }
]
```

**Python:**

```python
from json2sprite import process_json_file

process_json_file("input/flag.json", "output/flag.png")
```

## Reverse Conversion: PNG to JSON

### Example 4: Single PNG to JSON

**Command:**

```bash
json2sprite --reverse output/heart.png
```

**Output:** `output_json/heart.json` - Extracted sprite data

**Python:**

```python
from json2sprite import png_to_sprite, png_to_json_file

# Get sprite data as dictionary
sprite_data = png_to_sprite("output/heart.png", pixel_size=16)
print(sprite_data)

# Or save directly to JSON file
png_to_json_file("output/heart.png", "converted/heart.json", pixel_size=16)
```

### Example 5: Custom Pixel Size

If you created sprites with a different pixel size:

**Command:**

```bash
json2sprite --reverse output/tiny_sprite.png --pixel-size 8
```

**Python:**

```python
from json2sprite import png_to_sprite

# For 8x8 pixel sprites
sprite_data = png_to_sprite("output/tiny_sprite.png", pixel_size=8)
```

### Example 6: Batch Convert Folder

**Command:**

```bash
json2sprite --reverse output/
```

**Python:**

```python
from json2sprite import png_folder_to_json

png_folder_to_json("output/", "converted/", pixel_size=16)
```

### Example 7: Split Spritesheet

If you have a horizontal spritesheet and want to extract individual sprites:

**Python:**

```python
from json2sprite import split_spritesheet

sprites = split_spritesheet(
    sheet_path="output/characters.png",
    output_folder="split/",
    sprite_width=80,      # Each sprite is 80 pixels wide (5 cells × 16 pixels)
    sprite_height=80,     # Each sprite is 80 pixels tall
    padding=4,            # 4 pixels between sprites
    pixel_size=16         # Original pixel size
)

print(f"Extracted {len(sprites)} sprites")
# Each sprite is saved as split/sprite_000.json, split/sprite_001.json, etc.
```

## Round-Trip Conversion

### Example 8: JSON → PNG → JSON

Verify that conversion works both ways:

**Python:**

```python
import json
from json2sprite import process_json_file, png_to_json_file

# Original JSON
original_file = "input/heart.json"

# Convert to PNG
process_json_file(original_file, "temp/heart.png")

# Convert back to JSON
png_to_json_file("temp/heart.png", "temp/heart_converted.json", pixel_size=16)

# Compare
with open(original_file) as f1, open("temp/heart_converted.json") as f2:
    original = json.load(f1)
    converted = json.load(f2)
    
    print("Grid matches:", original[0]["grid"] == converted[0]["grid"])
    print("Colors preserved:", 
          all(original[0]["palette"][k] == converted[0]["palette"].get(k) 
              for k in original[0]["palette"]))
```

## Advanced Usage

### Example 9: Programmatic Sprite Generation

**Python:**

```python
from json2sprite import render_sprite, make_spritesheet

# Generate sprites programmatically
def generate_color_palette():
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
    sprites = []
    
    for i, color in enumerate(colors):
        sprite = {
            "sprite_name": f"color_{i}",
            "grid": ["####", "####", "####", "####"],
            "palette": {"#": color}
        }
        sprites.append(sprite)
    
    return sprites

# Create palette spritesheet
sprites = generate_color_palette()
sheet = make_spritesheet(sprites, pixel_size=16, padding=2)
sheet.save("palette.png")
```

### Example 10: Dynamic Sprite Editing

**Python:**

```python
from json2sprite import png_to_sprite, render_sprite

# Load sprite from PNG
sprite_data = png_to_sprite("output/heart.png", pixel_size=16)

# Modify the sprite (change color)
sprite_data["palette"]["#"] = "#00FF00"  # Change red to green

# Re-render
img = render_sprite(sprite_data, pixel_size=16)
img.save("output/green_heart.png")
```

### Example 11: Sprite Analysis

**Python:**

```python
from json2sprite import png_to_sprite

sprite_data = png_to_sprite("output/character.png", pixel_size=16)

# Analyze sprite
print(f"Sprite name: {sprite_data['sprite_name']}")
print(f"Dimensions: {len(sprite_data['grid'][0])}x{len(sprite_data['grid'])}")
print(f"Number of colors: {len(sprite_data['palette'])}")
print(f"Colors used:")
for char, color in sprite_data['palette'].items():
    if color != "transparent":
        print(f"  {char}: {color}")
```

### Example 12: Batch Processing with Custom Logic

**Python:**

```python
from pathlib import Path
from json2sprite import png_to_sprite, render_sprite

def invert_sprite_colors(png_path, output_path, pixel_size=16):
    """Convert sprite colors to their inverse."""
    sprite = png_to_sprite(png_path, pixel_size=pixel_size)
    
    # Invert colors
    for char, color in sprite["palette"].items():
        if color != "transparent" and color.startswith("#"):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            inv_r, inv_g, inv_b = 255 - r, 255 - g, 255 - b
            sprite["palette"][char] = f"#{inv_r:02X}{inv_g:02X}{inv_b:02X}"
    
    # Render inverted sprite
    img = render_sprite(sprite, pixel_size=pixel_size)
    img.save(output_path)

# Process all sprites in a folder
input_folder = Path("output/")
output_folder = Path("inverted/")
output_folder.mkdir(exist_ok=True)

for png_file in input_folder.glob("*.png"):
    output_file = output_folder / png_file.name
    invert_sprite_colors(png_file, output_file)
    print(f"Inverted: {png_file.name}")
```

## CLI Workflow Examples

### Workflow 1: Create, Convert, Verify

```bash
# 1. Create sprites from JSON
json2sprite input/

# 2. Convert back to verify
json2sprite --reverse output/

# 3. Compare files
diff input/sprite.json output_json/sprite.json
```

### Workflow 2: Design Pipeline

```bash
# 1. Design sprites (create JSON files in design/)
# 2. Generate PNGs for use in game
json2sprite design/ --output game_assets/

# 3. Later, if you need to modify
json2sprite --reverse game_assets/sprite.png
# 4. Edit the JSON
# 5. Regenerate
json2sprite output_json/sprite.json
```

### Workflow 3: Spritesheet Management

```bash
# 1. Create individual sprite JSONs
ls sprites/
# sprite_001.json, sprite_002.json, sprite_003.json

# 2. Combine into spritesheet
# (First combine JSONs into one array manually or with script)

# 3. Later, split back if needed
# Use Python API for split_spritesheet()
```

## Integration Examples

### Example 13: Game Asset Pipeline

**Python:**

```python
from json2sprite import process_folder, png_folder_to_json
from pathlib import Path

class SpriteAssetPipeline:
    def __init__(self, design_folder, output_folder, backup_folder):
        self.design = Path(design_folder)
        self.output = Path(output_folder)
        self.backup = Path(backup_folder)
    
    def build_assets(self):
        """Convert all JSON designs to PNG game assets."""
        print("Building game assets...")
        process_folder(self.design, self.output)
    
    def backup_designs(self):
        """Backup by reverse-converting PNGs to JSON."""
        print("Creating design backups...")
        png_folder_to_json(self.output, self.backup)
    
    def verify_integrity(self):
        """Verify round-trip conversion works."""
        # Implementation left as exercise
        pass

# Usage
pipeline = SpriteAssetPipeline("design/", "game/assets/", "backup/")
pipeline.build_assets()
pipeline.backup_designs()
```

## Tips and Best Practices

1. **Pixel Size Consistency**: Always use the same pixel_size for forward and reverse conversion
2. **Color Limits**: The reverse conversion supports up to 36 unique colors by default (A-Z, 0-9)
3. **Transparency**: Use "." or any character mapped to "transparent" for transparent pixels
4. **Naming**: Sprite names in JSON are derived from filenames
5. **Validation**: Always verify round-trip conversion for critical sprites

## Common Use Cases

- **Game Development**: Create and manage sprite assets
- **Pixel Art Tools**: Convert between formats
- **Asset Pipeline**: Automate sprite generation
- **Version Control**: Store sprites as text (JSON) instead of binary (PNG)
- **Sprite Analysis**: Extract and analyze sprite data programmatically
- **Batch Processing**: Convert entire directories efficiently
