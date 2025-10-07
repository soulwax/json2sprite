# File: tests/conftest.py

"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture(autouse=True)
def reset_sys_argv():
    """Reset sys.argv after each test to avoid side effects."""
    import sys

    original_argv = sys.argv.copy()
    yield
    sys.argv = original_argv
