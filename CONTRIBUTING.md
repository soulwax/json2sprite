# Contributing to json2sprite

Thank you for your interest in contributing to json2sprite! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage contributions
- Focus on constructive feedback
- Maintain professional communication

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/soulwax/json2sprite/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant code samples or error messages

### Suggesting Enhancements

1. Check if the enhancement has been suggested in [Issues](https://github.com/soulwax/json2sprite/issues)
2. Create a new issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach (optional)

### Pull Requests

1. **Fork the repository** and create your branch from `main`:

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Set up your development environment**:

   ```bash
   # On Unix/Linux/Mac
   ./setup_dev.sh
   
   # On Windows
   .\setup_dev.ps1
   ```

3. **Make your changes**:
   - Write clear, self-documenting code
   - Add docstrings to functions and classes
   - Follow the existing code style

4. **Add tests**:
   - Write tests for new functionality
   - Ensure all tests pass:

     ```bash
     pytest
     ```

   - Aim for high test coverage:

     ```bash
     pytest --cov=json2sprite --cov-report=html
     ```

5. **Format and lint your code**:

   ```bash
   # Format with Black
   black src/ tests/
   
   # Lint with Pylint
   pylint src/json2sprite/
   
   # Type check with mypy
   mypy src/json2sprite/
   ```

6. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference issue numbers when applicable

   ```bash
   git commit -m "Add feature X to handle Y (#issue-number)"
   ```

7. **Push to your fork**:

   ```bash
   git push origin feature/my-new-feature
   ```

8. **Open a Pull Request**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use Black for code formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Testing

- Write unit tests for all new functionality
- Use pytest fixtures for common test data
- Aim for >80% code coverage
- Test edge cases and error conditions

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update relevant documentation files
- Include code examples for new features

### Commit Messages

Good commit messages help understand the project history:

```
Add support for custom pixel sizes

- Add pixel_size parameter to render_sprite()
- Update tests to cover new parameter
- Document usage in README

Closes #123
```

### Branch Naming

Use descriptive branch names:

- `feature/description` - for new features
- `bugfix/description` - for bug fixes
- `docs/description` - for documentation changes
- `refactor/description` - for code refactoring

## Testing Locally

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_core.py
```

### Run With Coverage

```bash
pytest --cov=json2sprite --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Run Code Quality Checks

```bash
# Check formatting
black --check src/ tests/

# Lint
pylint src/json2sprite/

# Type check
mypy src/json2sprite/
```

## Building the Package

To test the package build:

```bash
python -m build
twine check dist/*
```

## Questions?

If you have questions or need help:

- Open an issue for discussion
- Check existing issues and documentation
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the AGPL-3.0-or-later License.
