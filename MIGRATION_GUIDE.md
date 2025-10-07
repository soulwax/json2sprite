# Migration Guide: Converting to PyPI Package Structure

This guide will help you restructure your existing json2sprite project into a proper PyPI package.

## Step 1: Backup Current Project

```bash
# Create a backup
cp -r json2sprite json2sprite_backup
```

## Step 2: Create New Directory Structure

```bash
# Navigate to your project
cd json2sprite

# Create the new structure
mkdir -p src/json2sprite
mkdir -p tests
mkdir -p .github/workflows
```

## Step 3: Move and Rename Files

### Move Python Files

```bash
# Move the main script and split it into modules
# You'll need to manually split json2sprite.py into:
# - src/json2sprite/__init__.py
# - src/json2sprite/core.py
# - src/json2sprite/processor.py
# - src/json2sprite/cli.py
```

### Keep Example Files

```bash
# Keep input/ and output/ directories as they are
# These will be useful for testing
```

## Step 4: Create New Configuration Files

Create these files in your project root (use the artifacts I provided):

1. **pyproject.toml** - Main package configuration
2. **MANIFEST.in** - Include additional files in distribution
3. **.github/workflows/ci.yml** - CI/CD configuration
4. **.codecov.yml** - Code coverage configuration
5. **CONTRIBUTING.md** - Contribution guidelines
6. **setup_dev.sh** - Unix setup script
7. **setup_dev.ps1** - Windows setup script

## Step 5: Update .gitignore

Your existing `.gitignore` is good, but make sure it includes:

```gitignore
# Distribution / packaging
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
htmlcov/
.coverage
coverage.xml

# IDEs
.vscode/
.idea/
```

## Step 6: Update README.md

Replace your README.md with the updated version that includes:

- Installation instructions
- API documentation
- Development setup
- CI badges

## Step 7: Create Test Files

Create these test files (use the artifacts I provided):

- `tests/conftest.py`
- `tests/test_init.py`
- `tests/test_core.py`
- `tests/test_processor.py`
- `tests/test_cli.py`

## Step 8: Update requirements.txt

Your current `requirements.txt` is fine, but the package now uses `pyproject.toml` for dependency management:

```txt
pillow>=10.0.0
```

Development dependencies are defined in `pyproject.toml` under `[project.optional-dependencies]`.

## Step 9: Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Restructure as PyPI package"
```

## Step 10: Set Up Development Environment

### On Windows (PowerShell)

```powershell
.\setup_dev.ps1
```

### On Unix/Linux/Mac

```bash
chmod +x setup_dev.sh
./setup_dev.sh
```

## Step 11: Run Tests

```bash
# Activate virtual environment first
# Windows:
.\.venv\Scripts\Activate.ps1
# Unix/Linux/Mac:
source .venv/bin/activate

# Run tests
pytest

# Run with coverage
pytest --cov=json2sprite --cov-report=html
```

## Step 12: Format and Lint Code

```bash
# Format code
black src/ tests/

# Lint code
pylint src/json2sprite/

# Type check
mypy src/json2sprite/
```

## Step 13: Build the Package

```bash
# Install build tools (if not already installed)
pip install build twine

# Build
python -m build

# Check
twine check dist/*
```

## Step 14: Set Up GitHub Repository

1. Create a new repository on GitHub (or use existing)
2. Push your code:

```bash
git remote add origin https://github.com/yourusername/json2sprite.git
git branch -M main
git push -u origin main
```

## Step 15: Enable GitHub Actions

Once you push, GitHub Actions will automatically run:

- Code formatting checks (Black)
- Linting (Pylint)
- Type checking (mypy)
- Tests (pytest) on multiple Python versions and OSes
- Package building

## Step 16: Set Up Codecov (Optional)

1. Go to [codecov.io](https://codecov.io/)
2. Sign in with GitHub
3. Enable your json2sprite repository
4. GitHub Actions will automatically upload coverage reports

## Step 17: Publish to PyPI (When Ready)

### Test PyPI First

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ json2sprite
```

### Publish to Real PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Test installation
pip install json2sprite
```

## Checklist

- [ ] Backed up original project
- [ ] Created new directory structure
- [ ] Moved and reorganized Python files
- [ ] Created all configuration files
- [ ] Created all test files
- [ ] Updated README.md
- [ ] Set up development environment
- [ ] All tests passing
- [ ] Code formatted with Black
- [ ] No Pylint errors
- [ ] Type checking passes
- [ ] Package builds successfully
- [ ] Pushed to GitHub
- [ ] CI/CD passing on GitHub Actions
- [ ] (Optional) Codecov configured
- [ ] (When ready) Published to PyPI

## Troubleshooting

### Tests failing?

- Check that all imports are correct
- Ensure virtual environment is activated
- Install dev dependencies: `pip install -e ".[dev]"`

### Black formatting issues?

- Run: `black src/ tests/`
- Check line length setting (100 in pyproject.toml)

### Pylint errors?

- Fix any code quality issues
- You can disable specific rules in pyproject.toml if needed
- Aim for score >8.0

### Import errors?

- Make sure you're in the project root
- Check that virtual environment is activated
- Reinstall: `pip install -e ".[dev]"`

### GitHub Actions failing?

- Check the logs in the Actions tab
- Test locally first with the same commands
- Ensure all dependencies are in pyproject.toml

## File Structure Comparison

### Before (Old Structure)

```plaintext
json2sprite/
├── .gitignore
├── json2sprite.py          # Single file
├── LICENSE.md
├── README.md
├── requirements.txt
├── tree.txt
├── input/
│   └── example1.json
└── output/
    └── example1.png
```

### After (New Structure)

```plaintext
json2sprite/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── json2sprite/
│       ├── __init__.py
│       ├── core.py
│       ├── processor.py
│       └── cli.py
├── tests/
│   ├── conftest.py
│   ├── test_init.py
│   ├── test_core.py
│   ├── test_processor.py
│   └── test_cli.py
├── input/
│   └── example1.json
├── output/
│   └── example1.png
├── .codecov.yml
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE.md
├── MANIFEST.in
├── MIGRATION_GUIDE.md
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup_dev.ps1
└── setup_dev.sh
```

## Benefits of New Structure

1. **Proper Python Package**: Can be installed via pip
2. **Automated Testing**: CI/CD runs tests on every push
3. **Code Quality**: Automated formatting and linting checks
4. **Better Organization**: Separated concerns (core, processor, CLI)
5. **Type Safety**: Type hints with mypy checking
6. **Documentation**: Comprehensive README and contributing guide
7. **Cross-platform**: Works on Windows, Linux, and macOS
8. **Professional**: Follows Python packaging best practices

## Next Steps After Migration

1. **Write More Tests**: Increase coverage to >90%
2. **Add More Features**:
   - CLI arguments for pixel_size and padding
   - Support for vertical spritesheets
   - Animation frame support
   - JSON schema validation
3. **Documentation**:
   - Add usage examples
   - Create tutorials
   - API documentation with Sphinx
4. **Community**:
   - Set up issue templates
   - Create pull request template
   - Add changelog
5. **Release**:
   - Version tagging
   - Release notes
   - PyPI publication

## Getting Help

If you encounter issues during migration:

1. Check this guide carefully
2. Review the artifacts provided
3. Look at similar projects on GitHub
4. Ask in the repository issues

Good luck with your migration! Feel free to reach out for help.
