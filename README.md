# Json2Sprite

A tool to convert JSON data into sprite images.

## Features

- Converts JSON data into sprite images.
- Easy to use command-line interface.
- Goals include support for many interpretations of JSON data for sprite generation.

## Installation

To install Json2Sprite, clone the repository and run the setup script:

```bash
git clone https://github.com/soulwax/json2sprite.git
cd json2sprite
pip install -r requirements.txt
```

json2sprite
=========

A tiny Python utility that converts JSON sprite descriptions into PNG images and simple spritesheets.

Features
--------

- Render individual sprites defined as a grid and palette in JSON into PNG images.
- Combine multiple sprites (JSON array) into a horizontal spritesheet with configurable pixel scale and padding.
- Transparent pixels supported via a "transparent" palette value or missing palette key.

Quick example
-------------

Place a JSON file like `input/example1.json` then run the script to generate `output/example1.png`.
json2sprite
==========

Small utility to render sprites from JSON into PNG images and simple horizontal spritesheets.

What it does
------------

- Render a single sprite (grid + palette) to PNG.
- Combine multiple sprite objects (JSON list) into a horizontal spritesheet.
- Supports transparent cells via the literal value "transparent" in the palette or by omitting a palette key.

Minimal JSON shape
------------------

Single sprite object (example):

{
  "grid": ["..R..", ".RRR.", "RRRRR"],
  "palette": {".": "transparent", "R": "#FF0000"}
}

Or a top-level list of objects to produce a single spritesheet.

Usage
-----

- Process a single file:

```powershell
python json2sprite.py input\example1.json
```

- Process a folder (mirrors into `output/`):

```powershell
python json2sprite.py input
```

Output
------

- By default PNGs are written under `output/`. Single-file input produces `output/<name>.png`. Folder input preserves relative paths and replaces `.json` with `.png`.

Setup (Windows PowerShell)
--------------------------

1) Create and activate a venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, allow local scripts once (run as admin) or use `Activate.bat` instead:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

2) Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Notes
-----

- Colors must be hex strings like `#RRGGBB`.
- `pixel_size` and `padding` are configured in the script (`render_sprite` / `make_spritesheet`) if you need different output scale.
- The script depends only on Pillow; add CLI flags or tests as needed.

License
-------

AGPL-3.0 License. See [LICENSE](LICENSE) for details.
