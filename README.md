# json2sprite

[![CI](https://github.com/soulwax/json2sprite/actions/workflows/ci.yml/badge.svg)](https://github.com/soulwax/json2sprite/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/soulwax/json2sprite/branch/main/graph/badge.svg)](https://codecov.io/gh/soulwax/json2sprite)
[![PyPI version](https://badge.fury.io/py/json2sprite.svg)](https://badge.fury.io/py/json2sprite)
[![Python versions](https://img.shields.io/pypi/pyversions/json2sprite.svg)](https://pypi.org/project/json2sprite/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

A robust Python utility that converts JSON sprite descriptions into PNG images and horizontal spritesheets.

## Features

- ✨ Render individual sprites defined as a grid and palette in JSON into PNG images
- 🖼️ Combine multiple sprites (JSON array) into a horizontal spritesheet with configurable pixel scale and padding
- 🎨 Transparent pixels supported via "transparent" palette value or missing palette key
- 🧪 Fully tested with pytest (100% coverage goal)
- 🔍 Type hints and comprehensive error handling
- 📦 Installable via pip
- 🔧 Command-line interface and Python API

## Installation

### From PyPI (when published)

```bash
pip install json2sprite
```

### From source

```bash
git clone https://github.com/soulwax/json2sprite.git
cd json2sprite
pip install -e ".[dev]"
```

## Quick Start

### Command Line Usage

Process a single JSON file:

```bash
json2sprite input/example1.json
```

Process an entire folder (maintains directory structure):

```bash
json2sprite input/
```

### Python API Usage

```python
from json2sprite import render_sprite, make_spritesheet
from PIL import Image

# Define a sprite
sprite_data = {
    "grid": [
        "..R..",
        ".RRR.",
        "RRRRR"
    ],
    "palette": {
        ".": "transparent",
        "R": "#FF0000"
    }
}

# Render single sprite
img = render_sprite(sprite_data, pixel_size=16)
img.save("output.png")

# Create spritesheet from multiple sprites
sprites = [sprite_data, sprite_data, sprite_data]
sheet = make_spritesheet(sprites, pixel_size=16, padding=4)
sheet.save("spritesheet.png")
```

## JSON Format

### Single Sprite Object

```json
{
  "grid": [
    "..R..",
    ".RRR.",
    "RRRRR"
  ],
  "palette": {
    ".": "transparent",
    "R": "#FF0000"
  }
}
```

### Multiple Sprites (Spritesheet)

```json
[
  {
    "sprite_name": "fireball",
    "grid": ["..R..", ".RRR."],
    "palette": {".": "transparent", "R": "#FF3C00"}
  },
  {
    "sprite_name": "knight",
    "grid": ["..B..", ".BBB."],
    "palette": {".": "transparent", "B": "#2C5FFF"}
  }
]
```

## Output

By default, PNG files are written to the `output/` directory:

- Single-file input produces `output/<name>.png`
- Folder input preserves relative paths and replaces `.json` with `.png`

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/soulwax/json2sprite.git
cd json2sprite

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On Linux/Mac:
source .venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=json2sprite --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code with Black
black src/ tests/

# Check code style
black --check src/ tests/

# Lint with Pylint
pylint src/json2sprite/

# Type check with mypy
mypy src/json2sprite/
```

### Building the Package

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Check the package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
json2sprite/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
├── src/
│   └── json2sprite/
│       ├── __init__.py     # Package initialization
│       ├── core.py         # Core rendering functions
│       ├── processor.py    # File processing utilities
│       └── cli.py          # Command-line interface
├── tests/
│   ├── conftest.py         # Pytest configuration
│   ├── test_core.py        # Core functionality tests
│   ├── test_processor.py   # File processing tests
│   ├── test_cli.py         # CLI tests
│   └── test_init.py        # Package tests
├── input/                  # Example input files
├── output/                 # Generated output files
├── .gitignore
├── LICENSE.md
├── MANIFEST.in
├── README.md
├── pyproject.toml          # Package configuration
└── requirements.txt        # Runtime dependencies
```

## Configuration

The following parameters can be adjusted:

- `pixel_size`: Scale factor for output images (default: 16)
- `padding`: Pixels between sprites in spritesheet (default: 4)

These can be configured in the code or by modifying the function calls in your script.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Run tests (`pytest`)
4. Run code quality checks (`black`, `pylint`, `mypy`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## License

This project is licensed under the GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE.md](LICENSE.md) for details.

## Author

soulwax@github

## Acknowledgments

- Built with [Pillow](https://python-pillow.org/) for image processing
- Tested with [pytest](https://pytest.org/)
- Code formatting with [Black](https://black.readthedocs.io/)
- Linting with [Pylint](https://pylint.org/)
