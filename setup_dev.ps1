# File: setup_dev.ps1

# Development setup script for Windows PowerShell

$ErrorActionPreference = "Stop"

Write-Host "Setting up json2sprite development environment..." -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install package in editable mode with dev dependencies
Write-Host "Installing package in development mode..." -ForegroundColor Yellow
pip install -e ".[dev]"

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  pytest                    # Run tests" -ForegroundColor White
Write-Host "  pytest --cov             # Run tests with coverage" -ForegroundColor White
Write-Host "  black src\ tests\        # Format code" -ForegroundColor White
Write-Host "  pylint src\json2sprite\  # Lint code" -ForegroundColor White
Write-Host "  mypy src\json2sprite\    # Type check" -ForegroundColor White
Write-Host "  python -m build          # Build package" -ForegroundColor White
