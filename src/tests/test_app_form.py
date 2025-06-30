"""Test Flask app form functionality."""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from mathviber.app import create_app


@pytest.fixture
def app() -> Flask:
    """Create a Flask app instance for testing.

    Returns:
        Flask: Test Flask application.
    """
    return create_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask app.

    Args:
        app: Flask application fixture.

    Returns:
        FlaskClient: Test client for making requests.
    """
    return app.test_client()


def test_form_submission_get(client: FlaskClient) -> None:
    """Test GET request shows the form without submitted text.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Enter a mathematical expression:" in response.data
    assert b"Function: y =" not in response.data  # Should not show result section


def test_form_submission_post_with_data(client: FlaskClient) -> None:
    """Test POST request with valid mathematical expression.

    Args:
        client: Flask test client.
    """
    test_input = "x**2"
    response = client.post("/", data={"user_input": test_input})

    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert test_input.encode() in response.data


def test_form_submission_post_empty_data(client: FlaskClient) -> None:
    """Test POST request with empty form data.

    Args:
        client: Flask test client.
    """
    response = client.post("/", data={"user_input": ""})

    assert response.status_code == 200
    # Empty input should not show the result section
    assert b"Function: y =" not in response.data


def test_form_submission_post_whitespace_data(client: FlaskClient) -> None:
    """Test POST request with whitespace-only data.

    Args:
        client: Flask test client.
    """
    response = client.post("/", data={"user_input": "   "})

    assert response.status_code == 200
    # Whitespace-only input should not show the result section (stripped)
    assert b"Function: y =" not in response.data


def test_form_submission_post_mathematical_expression(client: FlaskClient) -> None:
    """Test POST request with a mathematical expression.

    Args:
        client: Flask test client.
    """
    test_input = "x**2 + 2*x + 1"
    response = client.post("/", data={"user_input": test_input})

    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert test_input.encode() in response.data


def test_form_preserves_input_value(client: FlaskClient) -> None:
    """Test that the form preserves the input value after submission.

    Args:
        client: Flask test client.
    """
    test_input = "sin(x)"
    response = client.post("/", data={"user_input": test_input})

    assert response.status_code == 200
    # Check that the input field contains the submitted value
    assert (
        f'value="{test_input}"'.encode() in response.data
        or test_input.encode() in response.data
    )


def test_form_handles_special_characters(client: FlaskClient) -> None:
    """Test that the form handles mathematical constants correctly.

    Args:
        client: Flask test client.
    """
    test_input = "sin(pi/2) + cos(0)"
    response = client.post("/", data={"user_input": test_input})

    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert test_input.encode() in response.data
