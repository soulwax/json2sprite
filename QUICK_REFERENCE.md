# Quick Reference Guide

## Installation

```bash
# From source (development)
git clone https://github.com/soulwax/json2sprite.git
cd json2sprite
pip install -e ".[dev]"

# From PyPI (when published)
pip install json2sprite
```

## Basic Usage

### Command Line

```bash
# Single file
json2sprite input/sprite.json

# Folder (recursive)
json2sprite input/

# The output will be in the output/ directory
```

### Python API

```python
from json2sprite import render_sprite, make_spritesheet

# Single sprite
sprite = {
    "grid": ["RGB", "GBR"],
    "palette": {"R": "#FF0000", "G": "#00FF00", "B": "#0000FF"}
}
img = render_sprite(sprite, pixel_size=16)
img.save("my_sprite.png")

# Multiple sprites (spritesheet)
sprites = [sprite1, sprite2, sprite3]
sheet = make_spritesheet(sprites, pixel_size=16, padding=4)
sheet.save("my_spritesheet.png")
```

## Development Commands

### Setup

```bash
# Windows
.\setup_dev.ps1

# Unix/Linux/Mac
./setup_dev.sh
```

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=json2sprite --cov-report=html

# Specific test file
pytest tests/test_core.py

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint code
pylint src/json2sprite/

# Type check
mypy src/json2sprite/

# Run all checks
black src/ tests/ && pylint src/json2sprite/ && mypy src/json2sprite/ && pytest
```

### Building

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add my feature"

# Push to GitHub
git push origin feature/my-feature

# After PR is merged, update main
git checkout main
git pull origin main
```

## JSON Format

### Minimal Example

```json
[
  {
    "grid": ["RRR", "RRR", "RRR"],
    "palette": {
      "R": "#FF0000"
    }
  }
]
```

### With Transparency

```json
[
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
]
```

### Multiple Sprites

```json
[
  {
    "sprite_name": "red_square",
    "grid": ["RR", "RR"],
    "palette": {"R": "#FF0000"}
  },
  {
    "sprite_name": "green_square",
    "grid": ["GG", "GG"],
    "palette": {"G": "#00FF00"}
  }
]
```

## Common Issues

### Import Error

```bash
# Make sure package is installed in editable mode
pip install -e ".[dev]"
```

### Tests Failing

```bash
# Reinstall dependencies
pip install -e ".[dev]"

# Clear pytest cache
pytest --cache-clear
```

### Black Formatting

```bash
# Auto-fix all formatting
black src/ tests/
```

### Pylint Score Low

```bash
# Get detailed report
pylint src/json2sprite/ --reports=y
```

## Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## CI/CD

GitHub Actions automatically runs on every push:
- Black formatting check
- Pylint (score ≥ 8.0)
- mypy type checking
- pytest on Python 3.8-3.12
- Tests on Ubuntu, Windows, macOS

## File Locations

- Source code: `src/json2sprite/`
- Tests: `tests/`
- Configuration: `pyproject.toml`
- CI/CD: `.github/workflows/ci.yml`
- Input examples: `input/`
- Output: `output/` (auto-created)

## Useful Links

- Repository: https://github.com/soulwax/json2sprite
- Issues: https://github.com/soulwax/json2sprite/issues
- PyPI: https://pypi.org/project/json2sprite/ (when published)
- Documentation: See README.md

## Version Information

```python
import json2sprite
print(json2sprite.__version__)
```

## Getting Help

1. Check README.md
2. Search existing issues
3. Create new issue with bug/feature template
4. See CONTRIBUTING.md for detailed guidelines