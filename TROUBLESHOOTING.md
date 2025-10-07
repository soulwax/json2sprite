# Troubleshooting Guide

## Installation Issues

### Problem: `pip install -e .` fails

**Symptoms:**

- `ModuleNotFoundError: No module named 'json2sprite'`
- Package not found errors
- Import errors in tests

**Solutions:**

1. **Ensure you're in the project root directory:**

   ```bash
   cd /path/to/json2sprite
   ls -la  # Should see pyproject.toml, setup.py, src/, tests/
   ```

2. **Clean previous builds:**

   ```bash
   # Remove old build artifacts
   rm -rf build/ dist/ src/*.egg-info
   # On Windows:
   # rmdir /s /q build dist
   # del /s /q src\*.egg-info
   ```

3. **Upgrade pip and setuptools:**

   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

4. **Install with verbose output:**

   ```bash
   pip install -e . -v
   ```

5. **Check Python version:**

   ```bash
   python --version  # Should be 3.8 or higher
   ```

### Problem: Tests fail with import errors

**Symptoms:**

- `ModuleNotFoundError: No module named 'json2sprite'`
- Tests can't find the package

**Solutions:**

1. **Install in editable mode with dev dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

2. **Verify installation:**

   ```bash
   pip list | grep json2sprite
   python -c "import json2sprite; print(json2sprite.__version__)"
   ```

3. **Check PYTHONPATH:**

   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   # Should include your project directory
   ```

### Problem: Pylint fails

**Symptoms:**

- Import errors in pylint
- "Unable to import" messages

**Solutions:**

1. **Install with dev dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

2. **Run from project root:**

   ```bash
   cd /path/to/json2sprite
   pylint src/json2sprite/
   ```

3. **Check pylint can find the package:**

   ```bash
   pylint --version
   python -c "import json2sprite"  # Should not error
   ```

## Testing Issues

### Problem: pytest not found

**Solution:**

```bash
pip install pytest pytest-cov
```

### Problem: Tests fail with "No module named 'json2sprite'"

**Solution:**

```bash
# Install package first
pip install -e .

# Then run tests
pytest
```

### Problem: Coverage reports are empty

**Solution:**

```bash
# Install coverage tools
pip install pytest-cov

# Run with explicit source
pytest --cov=src/json2sprite --cov-report=html
```

## Package Structure Issues

### Required File Structure

Your project MUST have this structure:

```
json2sprite/
├── pyproject.toml       # Required: Package configuration
├── setup.py             # Required: Compatibility shim
├── src/                 # Required: Source directory
│   └── json2sprite/     # Required: Package directory
│       ├── __init__.py  # Required: Package init
│       ├── py.typed     # Required: Type checking marker
│       ├── core.py
│       ├── processor.py
│       └── cli.py
└── tests/               # Required: Test directory
    ├── conftest.py
    ├── test_init.py
    ├── test_core.py
    ├── test_processor.py
    └── test_cli.py
```

### Missing Files Checklist

- [ ] `pyproject.toml` exists in root
- [ ] `setup.py` exists in root
- [ ] `src/json2sprite/__init__.py` exists
- [ ] `src/json2sprite/py.typed` exists
- [ ] All `*.py` files are in `src/json2sprite/`

## Common Mistakes

### 1. Wrong Working Directory

**Problem:** Running commands from wrong directory

**Solution:**

```bash
# Always run from project root
cd /path/to/json2sprite
pwd  # Should show .../json2sprite

# NOT from inside src/ or tests/
```

### 2. Virtual Environment Not Activated

**Problem:** Installing to system Python instead of venv

**Solution:**

```bash
# Activate venv first
# Windows:
.\.venv\Scripts\Activate.ps1
# Unix/Linux/Mac:
source .venv/bin/activate

# Verify:
which python  # Should point to .venv
```

### 3. Stale .pyc Files

**Problem:** Old bytecode interfering

**Solution:**

```bash
# Remove all .pyc files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# On Windows:
# del /s /q *.pyc
# for /d /r %i in (__pycache__) do @rmdir /s /q "%i"
```

### 4. Mixed Line Endings (Windows)

**Problem:** Scripts have wrong line endings

**Solution:**

```bash
# Convert to Unix line endings
dos2unix setup_dev.sh

# Or set git to auto-convert
git config core.autocrlf true
```

## Step-by-Step Recovery

If nothing works, follow these steps:

### 1. Clean Everything

```bash
# Remove all generated files
rm -rf build/ dist/ *.egg-info src/*.egg-info
rm -rf .pytest_cache/ htmlcov/ .coverage
rm -rf **/__pycache__/

# On Windows use:
# rmdir /s /q build dist .pytest_cache htmlcov
```

### 2. Check File Structure

```bash
# Verify critical files exist
ls pyproject.toml
ls setup.py
ls src/json2sprite/__init__.py
ls src/json2sprite/py.typed
```

### 3. Create Missing Files

If `setup.py` is missing:

```python
# File: setup.py
from setuptools import setup
setup()
```

If `py.typed` is missing:

```bash
touch src/json2sprite/py.typed
```

### 4. Fresh Virtual Environment

```bash
# Remove old venv
rm -rf .venv

# Create new venv
python -m venv .venv

# Activate
source .venv/bin/activate  # Unix
.\.venv\Scripts\Activate.ps1  # Windows

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel
```

### 5. Install Package

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 6. Verify Installation

```bash
# Check package is installed
pip list | grep json2sprite

# Test import
python -c "import json2sprite; print(json2sprite.__version__)"

# Should print: 0.1.0
```

### 7. Run Tests

```bash
pytest -v
```

## Environment Variables

### Set PYTHONPATH (if needed)

```bash
# Unix/Linux/Mac:
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"

# Windows (cmd):
set PYTHONPATH=%PYTHONPATH%;%CD%\src

# Windows (PowerShell):
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD\src"
```

## Platform-Specific Issues

### Windows

1. **PowerShell Execution Policy:**

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Path separators:**
   - Use `\` in paths or raw strings `r"path\to\file"`

3. **Encoding issues:**
   - Ensure files are UTF-8 encoded

### macOS

1. **Python version:**
   - Use `python3` not `python`
   - Check: `python3 --version`

2. **Permissions:**

   ```bash
   chmod +x setup_dev.sh
   ```

### Linux

1. **Python dev headers:**

   ```bash
   sudo apt-get install python3-dev  # Debian/Ubuntu
   sudo yum install python3-devel    # RHEL/CentOS
   ```

2. **Virtual environment:**

   ```bash
   sudo apt-get install python3-venv  # if venv missing
   ```

## Quick Diagnostic Script

Save as `diagnose.py` and run with `python diagnose.py`:

```python
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

print("=== JSON2SPRITE DIAGNOSTIC ===\n")

# Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}\n")

# Check critical files
critical_files = [
    "pyproject.toml",
    "setup.py",
    "src/json2sprite/__init__.py",
    "src/json2sprite/py.typed",
    "src/json2sprite/core.py",
    "src/json2sprite/processor.py",
    "src/json2sprite/cli.py",
]

print("Critical files check:")
for file in critical_files:
    exists = "✓" if Path(file).exists() else "✗"
    print(f"  {exists} {file}")

# Try importing
print("\nImport test:")
try:
    import json2sprite
    print(f"  ✓ json2sprite imported successfully")
    print(f"  Version: {json2sprite.__version__}")
except ImportError as e:
    print(f"  ✗ Failed to import: {e}")

# Check sys.path
print(f"\nPython path:")
for p in sys.path[:5]:
    print(f"  - {p}")

print("\n=== END DIAGNOSTIC ===")
```

## Still Having Issues?

1. **Check GitHub Issues:** <https://github.com/soulwax/json2sprite/issues>
2. **Create a bug report** with:
   - Output of `diagnose.py`
   - Complete error messages
   - Your OS and Python version
   - Steps you've already tried

## Quick Reference

```bash
# Full reset and reinstall
rm -rf .venv build dist *.egg-info src/*.egg-info
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
pytest -v
```
