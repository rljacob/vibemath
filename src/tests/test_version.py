"""Test version information."""

import re

from mathviber import __version__


def test_version_format() -> None:
    """Test that version follows semantic versioning format."""
    version_pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$"
    assert re.match(
        version_pattern, __version__
    ), f"Invalid version format: {__version__}"


def test_version_is_string() -> None:
    """Test that version is a string."""
    assert isinstance(__version__, str)


def test_version_not_empty() -> None:
    """Test that version is not empty."""
    assert __version__.strip()
