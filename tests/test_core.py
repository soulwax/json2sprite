# File: tests/test_core.py

"""Tests for core sprite rendering functionality."""

import pytest
from PIL import Image

from json2sprite.core import make_spritesheet, render_sprite


class TestRenderSprite:
    """Tests for render_sprite function."""

    def test_render_simple_sprite(self):
        """Test rendering a simple sprite."""
        sprite = {
            "grid": ["R..", ".R.", "..R"],
            "palette": {".": "transparent", "R": "#FF0000"},
        }
        img = render_sprite(sprite, pixel_size=1)

        assert img.size == (3, 3)
        assert img.mode == "RGBA"
        assert img.getpixel((0, 0)) == (255, 0, 0, 255)
        assert img.getpixel((1, 0)) == (0, 0, 0, 0)

    def test_render_with_scaling(self):
        """Test rendering with pixel scaling."""
        sprite = {
            "grid": ["R", "R"],
            "palette": {"R": "#00FF00"},
        }
        img = render_sprite(sprite, pixel_size=16)

        assert img.size == (16, 32)

    def test_missing_grid_key(self):
        """Test error when grid key is missing."""
        sprite = {"palette": {"R": "#FF0000"}}

        with pytest.raises(KeyError, match="grid"):
            render_sprite(sprite)

    def test_missing_palette_key(self):
        """Test error when palette key is missing."""
        sprite = {"grid": ["R"]}

        with pytest.raises(KeyError, match="palette"):
            render_sprite(sprite)

    def test_invalid_grid_type(self):
        """Test error when grid is not a list."""
        sprite = {"grid": "invalid", "palette": {}}

        with pytest.raises(ValueError, match="Grid must be"):
            render_sprite(sprite)

    def test_uneven_grid_rows(self):
        """Test error when grid rows have different lengths."""
        sprite = {
            "grid": ["RR", "R"],
            "palette": {"R": "#FF0000"},
        }

        with pytest.raises(ValueError, match="same length"):
            render_sprite(sprite)

    def test_invalid_color_format(self):
        """Test error with invalid color format."""
        sprite = {
            "grid": ["R"],
            "palette": {"R": "invalid"},
        }

        with pytest.raises(ValueError, match="Invalid color format"):
            render_sprite(sprite)

    def test_invalid_hex_color(self):
        """Test error with invalid hex color."""
        sprite = {
            "grid": ["R"],
            "palette": {"R": "#GGGGGG"},
        }

        with pytest.raises(ValueError, match="Invalid hex color"):
            render_sprite(sprite)

    def test_transparent_cells(self):
        """Test handling of transparent cells."""
        sprite = {
            "grid": ["R.", ".R"],
            "palette": {".": "transparent", "R": "#0000FF"},
        }
        img = render_sprite(sprite, pixel_size=1)

        assert img.getpixel((1, 0)) == (0, 0, 0, 0)
        assert img.getpixel((0, 0)) == (0, 0, 255, 255)

    def test_missing_palette_entry(self):
        """Test handling of missing palette entries (treated as transparent)."""
        sprite = {
            "grid": ["RX"],
            "palette": {"R": "#FF0000"},
        }
        img = render_sprite(sprite, pixel_size=1)

        assert img.getpixel((0, 0)) == (255, 0, 0, 255)
        assert img.getpixel((1, 0)) == (0, 0, 0, 0)


class TestMakeSpritesheet:
    """Tests for make_spritesheet function."""

    def test_single_sprite_sheet(self):
        """Test creating a spritesheet with one sprite."""
        sprites = [
            {"grid": ["RR", "RR"], "palette": {"R": "#FF0000"}},
        ]
        sheet = make_spritesheet(sprites, pixel_size=2, padding=0)

        assert sheet.size == (4, 4)
        assert sheet.mode == "RGBA"

    def test_multiple_sprites_sheet(self):
        """Test creating a spritesheet with multiple sprites."""
        sprites = [
            {"grid": ["R"], "palette": {"R": "#FF0000"}},
            {"grid": ["G"], "palette": {"G": "#00FF00"}},
        ]
        sheet = make_spritesheet(sprites, pixel_size=2, padding=4)

        expected_width = 2 + 4 + 2  # sprite1 + padding + sprite2
        assert sheet.size == (expected_width, 2)

    def test_empty_sprite_list(self):
        """Test error with empty sprite list."""
        with pytest.raises(ValueError, match="empty sprite list"):
            make_spritesheet([])

    def test_different_height_sprites(self):
        """Test spritesheet with different height sprites."""
        sprites = [
            {"grid": ["R"], "palette": {"R": "#FF0000"}},
            {"grid": ["G", "G"], "palette": {"G": "#00FF00"}},
        ]
        sheet = make_spritesheet(sprites, pixel_size=1, padding=1)

        assert sheet.size[1] == 2  # Height should be max of all sprites

    def test_padding_calculation(self):
        """Test correct padding between sprites."""
        sprites = [
            {"grid": ["R"], "palette": {"R": "#FF0000"}},
            {"grid": ["G"], "palette": {"G": "#00FF00"}},
            {"grid": ["B"], "palette": {"B": "#0000FF"}},
        ]
        sheet = make_spritesheet(sprites, pixel_size=1, padding=2)

        # 1 + 2 + 1 + 2 + 1 = 7 (sprite + padding + sprite + padding + sprite)
        assert sheet.size[0] == 7
