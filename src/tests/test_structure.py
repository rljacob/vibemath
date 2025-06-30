"""Test package structure and metadata."""

import importlib.util


def test_package_import() -> None:
    """Test that the mathviber package can be imported."""
    import mathviber

    assert mathviber is not None


def test_version_import() -> None:
    """Test that version can be imported from the package."""
    from mathviber import __version__

    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_app_module_exists() -> None:
    """Test that the app module exists and can be imported."""
    spec = importlib.util.find_spec("mathviber.app")
    assert spec is not None

    from mathviber.app import create_app

    assert create_app is not None


def test_cli_module_exists() -> None:
    """Test that the CLI module exists and can be imported."""
    spec = importlib.util.find_spec("mathviber.cli")
    assert spec is not None

    from mathviber.cli import main

    assert main is not None


def test_create_app_function() -> None:
    """Test that create_app function exists and returns a Flask app."""
    from flask import Flask

    from mathviber.app import create_app

    app = create_app()
    assert isinstance(app, Flask)
    assert app.name == "mathviber.app"


def test_main_function_exists() -> None:
    """Test that main function exists in app module."""
    from flask import Flask

    from mathviber.app import main

    app = main()
    assert isinstance(app, Flask)
