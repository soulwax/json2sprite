#!/bin/bash
# File: setup_dev.sh

set -e

echo "Setting up json2sprite development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install package in editable mode with dev dependencies
echo "Installing package in development mode..."
pip install -e ".[dev]"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "Useful commands:"
echo "  pytest                    # Run tests"
echo "  pytest --cov             # Run tests with coverage"
echo "  black src/ tests/        # Format code"
echo "  pylint src/json2sprite/  # Lint code"
echo "  mypy src/json2sprite/    # Type check"
echo "  python -m build          # Build package"
