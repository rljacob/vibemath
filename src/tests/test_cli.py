"""Test CLI functionality."""

from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from mathviber.cli import main


def test_main_with_version(capsys) -> None:
    """Test CLI version argument."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "MathViber" in captured.out
    assert "0.1.0" in captured.out


@patch("mathviber.app.main")
def test_main_default_args(mock_flask_main, capsys) -> None:
    """Test CLI with default arguments."""
    # Mock the Flask app
    mock_app = MagicMock(spec=Flask)
    mock_flask_main.return_value = mock_app

    result = main([])

    assert result == 0
    captured = capsys.readouterr()
    assert "MathViber" in captured.out
    assert "starting on 127.0.0.1:5000" in captured.out

    # Verify Flask app was created and run was called
    mock_flask_main.assert_called_once()
    mock_app.run.assert_called_once_with(host="127.0.0.1", port=5000, debug=False)


@patch("mathviber.app.main")
def test_main_custom_host_port(mock_flask_main, capsys) -> None:
    """Test CLI with custom host and port."""
    # Mock the Flask app
    mock_app = MagicMock(spec=Flask)
    mock_flask_main.return_value = mock_app

    result = main(["--host", "0.0.0.0", "--port", "8080"])

    assert result == 0
    captured = capsys.readouterr()
    assert "starting on 0.0.0.0:8080" in captured.out

    # Verify Flask app was created and run was called with correct args
    mock_flask_main.assert_called_once()
    mock_app.run.assert_called_once_with(host="0.0.0.0", port=8080, debug=False)


@patch("mathviber.app.main")
def test_main_debug_mode(mock_flask_main, capsys) -> None:
    """Test CLI with debug mode enabled."""
    # Mock the Flask app
    mock_app = MagicMock(spec=Flask)
    mock_flask_main.return_value = mock_app

    result = main(["--debug"])

    assert result == 0
    captured = capsys.readouterr()
    assert "Debug mode enabled" in captured.out

    # Verify Flask app was created and run was called with debug=True
    mock_flask_main.assert_called_once()
    mock_app.run.assert_called_once_with(host="127.0.0.1", port=5000, debug=True)


@patch("mathviber.app.main")
def test_main_returns_flask_app(mock_flask_main) -> None:
    """Test that main() creates and returns a Flask app through flask_main."""
    # Mock the Flask app
    mock_app = MagicMock(spec=Flask)
    mock_flask_main.return_value = mock_app

    # Call main without actually running the server
    main([])

    # Verify that flask_main was called and returns a Flask app
    mock_flask_main.assert_called_once()
    assert mock_flask_main.return_value == mock_app


def test_flask_main_import() -> None:
    """Test that flask_main can be imported from mathviber.app."""
    from flask import Flask

    from mathviber.app import main as flask_main

    app = flask_main()
    assert isinstance(app, Flask)
