"""Test Flask app home route functionality."""

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


def test_home_route_exists(client: FlaskClient) -> None:
    """Test that the home route exists and responds.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_home_route_content(client: FlaskClient) -> None:
    """Test that the home route returns HTML with MathViber content.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"MathViber" in response.data
    assert b"Mathematical Expression Visualizer" in response.data
    assert b'<form method="POST"' in response.data
    assert b'<input type="text"' in response.data
    assert b"Plot Function" in response.data
    assert b"Enter a mathematical expression:" in response.data
    assert b"Examples: sin(x), x**2" in response.data


def test_home_route_content_type(client: FlaskClient) -> None:
    """Test that the home route returns HTML content type.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")


def test_app_name(app: Flask) -> None:
    """Test that the app has the correct name.

    Args:
        app: Flask application fixture.
    """
    assert app.name == "mathviber.app"


def test_app_has_home_route(app: Flask) -> None:
    """Test that the app has the home route configured.

    Args:
        app: Flask application fixture.
    """
    # Check that the route exists by looking at the URL map
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/" in routes
