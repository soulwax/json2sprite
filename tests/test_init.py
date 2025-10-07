# File: tests/test_init.py

"""Tests for package initialization."""

import json2sprite


class TestPackageInit:
    """Tests for package-level exports."""

    def test_version_exists(self):
        """Test that version is defined."""
        assert hasattr(json2sprite, "__version__")
        assert isinstance(json2sprite.__version__, str)

    def test_author_exists(self):
        """Test that author is defined."""
        assert hasattr(json2sprite, "__author__")
        assert isinstance(json2sprite.__author__, str)

    def test_license_exists(self):
        """Test that license is defined."""
        assert hasattr(json2sprite, "__license__")
        assert json2sprite.__license__ == "AGPL-3.0-or-later"

    def test_all_exports(self):
        """Test that __all__ contains expected exports."""
        expected_exports = [
            "render_sprite",
            "make_spritesheet",
            "process_json_file",
            "process_folder",
        ]

        assert hasattr(json2sprite, "__all__")
        assert set(json2sprite.__all__) == set(expected_exports)

    def test_functions_accessible(self):
        """Test that main functions are accessible from package."""
        assert callable(json2sprite.render_sprite)
        assert callable(json2sprite.make_spritesheet)
        assert callable(json2sprite.process_json_file)
        assert callable(json2sprite.process_folder)
