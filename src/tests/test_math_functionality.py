"""Test mathematical expression functionality."""

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


def test_valid_mathematical_expressions(client: FlaskClient) -> None:
    """Test various valid mathematical expressions.

    Args:
        client: Flask test client.
    """
    valid_expressions = [
        "x**2",
        "sin(x)",
        "cos(x)",
        "exp(x)",
        "log(x + 1)",
        "sqrt(abs(x))",
        "x**3 + 2*x**2 + x + 1",
        "sin(x) + cos(x)",
        "exp(-x**2)",
    ]

    for expression in valid_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert expression.encode() in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for expression: {expression}"


def test_invalid_mathematical_expressions(client: FlaskClient) -> None:
    """Test invalid mathematical expressions that should show errors.

    Args:
        client: Flask test client.
    """
    invalid_expressions = [
        "import os",
        "exec('print(1)')",
        "__builtins__",
        "open('file.txt')",
        "unknown_function(x)",
        "x +",  # Syntax error
        "1/0 + x",  # Should cause evaluation error
    ]

    for expression in invalid_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert (
            b"Error:" in response.data
        ), f"Expected error for expression: {expression}"


def test_plot_generation_and_serving(client: FlaskClient) -> None:
    """Test that plots are generated and can be served.

    Args:
        client: Flask test client.
    """
    response = client.post("/", data={"user_input": "x**2"})
    assert response.status_code == 200
    assert b"Function: y =" in response.data

    # Check if plot image is referenced
    response_text = response.data.decode()
    if "plot_" in response_text:
        # Extract plot filename from the response
        import re

        plot_match = re.search(r"plot_([a-f0-9]+)\.png", response_text)
        if plot_match:
            filename = plot_match.group(0)

            # Test serving the plot image
            plot_response = client.get(f"/plot/{filename}")
            assert plot_response.status_code == 200
            assert plot_response.content_type == "image/png"

            # Test downloading the plot
            download_response = client.get(f"/download/{filename}")
            assert download_response.status_code == 200
            assert download_response.content_type == "image/png"


def test_plot_not_found(client: FlaskClient) -> None:
    """Test handling of non-existent plot files.

    Args:
        client: Flask test client.
    """
    response = client.get("/plot/nonexistent.png")
    assert response.status_code == 404
    assert b"Plot not found" in response.data

    response = client.get("/download/nonexistent.png")
    assert response.status_code == 404
    assert b"Plot not found" in response.data


def test_mathematical_constants(client: FlaskClient) -> None:
    """Test mathematical constants are properly recognized.

    Args:
        client: Flask test client.
    """
    constants_expressions = [
        "pi",
        "e",
        "sin(pi)",
        "exp(1)",
        "log(e)",
    ]

    for expression in constants_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for constant: {expression}"


def test_trigonometric_functions(client: FlaskClient) -> None:
    """Test trigonometric functions work correctly.

    Args:
        client: Flask test client.
    """
    trig_expressions = [
        "sin(x)",
        "cos(x)",
        "tan(x)",
        "arcsin(x/10)",  # Scaled to avoid domain errors
        "arccos(x/10)",
        "arctan(x)",
        "sinh(x/5)",  # Scaled to avoid overflow
        "cosh(x/5)",
        "tanh(x)",
    ]

    for expression in trig_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for trig function: {expression}"


def test_exponential_and_logarithmic_functions(client: FlaskClient) -> None:
    """Test exponential and logarithmic functions work correctly.

    Args:
        client: Flask test client.
    """
    exp_log_expressions = [
        "exp(x/5)",  # Scaled to avoid overflow
        "log(abs(x) + 1)",  # Avoid log of negative numbers
        "log10(abs(x) + 1)",
        "sqrt(abs(x))",
        "abs(x)",
    ]

    for expression in exp_log_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for exp/log function: {expression}"


def test_complex_mathematical_expressions(client: FlaskClient) -> None:
    """Test complex mathematical expressions.

    Args:
        client: Flask test client.
    """
    complex_expressions = [
        "sin(x) * cos(x)",
        "exp(-x**2) * sin(10*x)",
        "x**3 - 3*x**2 + 2*x - 1",
        "(x**2 + 1) / (x**2 + 2)",
        "sqrt(abs(sin(x)))",
    ]

    for expression in complex_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for complex expression: {expression}"


def test_power_operations(client: FlaskClient) -> None:
    """Test power operations with both ** and ^ syntax.

    Args:
        client: Flask test client.
    """
    power_expressions = [
        "x**2",
        "x**3",
        "x^2",  # Should be converted to **
        "2**x",
        "pow(x, 2)",
    ]

    for expression in power_expressions:
        response = client.post("/", data={"user_input": expression})
        assert response.status_code == 200
        assert b"Function: y =" in response.data
        assert (
            b"Error:" not in response.data
        ), f"Unexpected error for power expression: {expression}"
