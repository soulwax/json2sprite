# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-10-07

### Added on 2025-10-07

- **Reverse conversion**: PNG to JSON functionality
  - `png_to_sprite()` - Convert PNG image to sprite dictionary
  - `png_to_json_file()` - Convert PNG file to JSON file
  - `png_folder_to_json()` - Batch convert folder of PNGs to JSON
  - `split_spritesheet()` - Split horizontal spritesheet into individual sprites
- CLI support for reverse conversion with `--reverse` flag
- CLI option `--pixel-size` for specifying pixel size in reverse conversion
- Comprehensive test suite for reverse functionality (30+ new tests)
- Initial PyPI package structure
- Comprehensive test suite with pytest
- CI/CD pipeline with GitHub Actions
- Code quality checks (Black, Pylint, mypy)
- Command-line interface
- Python API for programmatic usage
- Documentation and contributing guidelines

## [0.3.0] - 2025-10-07

### Added on 2025-10-07

- **Reverse conversion**: PNG to JSON functionality
  - `png_to_sprite()` - Convert PNG image to sprite dictionary
  - `png_to_json_file()` - Convert PNG file to JSON file
  - `png_folder_to_json()` - Batch convert folder of PNGs to JSON
  - `split_spritesheet()` - Split horizontal spritesheet into individual sprites
- CLI support for reverse conversion with `--reverse` flag
- CLI option `--pixel-size` for specifying pixel size in reverse conversion
- Comprehensive test suite for reverse functionality (30+ new tests)
- Initial PyPI package structure
- Comprehensive test suite with pytest
- CI/CD pipeline with GitHub Actions
- Code quality checks (Black, Pylint, mypy)
- Command-line interface
- Python API for programmatic usage
- Documentation and contributing guidelines

## [0.2.0] - 2025-10-07

### Added on 2025-10-07

- Initial PyPI package structure
- Comprehensive test suite with pytest
- CI/CD pipeline with GitHub Actions
- Code quality checks (Black, Pylint, mypy)
- Command-line interface
- Python API for programmatic usage
- Documentation and contributing guidelines

### Changed

- Restructured project as proper Python package
- Split monolithic script into modules (core, processor, cli)
- Improved error handling and validation

### Fixed

- N/A

## [0.1.0] - 2025-10-07

### Added initial release on 2025-10-07

- Core sprite rendering functionality
- JSON to PNG conversion
- Spritesheet generation
- Transparent pixel support
- Configurable pixel size and padding
- Basic command-line interface

[0.1.0]: https://github.com/soulwax/json2sprite/releases/tag/v0.1.0
