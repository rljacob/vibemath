"""Test advanced plotting features."""

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


def test_custom_x_range(client: FlaskClient) -> None:
    """Test plotting with custom x range.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_min": "-5",
            "x_max": "5",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_custom_y_range(client: FlaskClient) -> None:
    """Test plotting with custom y range.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "y_min": "0",
            "y_max": "100",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_custom_axis_labels(client: FlaskClient) -> None:
    """Test plotting with custom axis labels.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_name": "Time (s)",
            "y_name": "Distance (m)",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_custom_graph_title(client: FlaskClient) -> None:
    """Test plotting with custom graph title.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "graph_title": "My Custom Graph",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_logarithmic_scales(client: FlaskClient) -> None:
    """Test plotting with logarithmic scales.

    Args:
        client: Flask test client.
    """
    # Test x-axis log scale
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_min": "0.1",
            "x_max": "100",
            "x_log": "true",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data

    # Test y-axis log scale
    response = client.post(
        "/",
        data={
            "user_input": "exp(x)",
            "y_log": "true",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data

    # Test both axes log scale
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_min": "1",
            "x_max": "100",
            "x_log": "true",
            "y_log": "true",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_invalid_x_range(client: FlaskClient) -> None:
    """Test error handling for invalid x range.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_min": "10",
            "x_max": "5",  # max < min
        },
    )
    assert response.status_code == 200
    assert b"Error:" in response.data
    assert b"X minimum must be less than X maximum" in response.data


def test_invalid_numeric_inputs(client: FlaskClient) -> None:
    """Test error handling for invalid numeric inputs.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "x_min": "invalid",
            "x_max": "10",
        },
    )
    assert response.status_code == 200
    assert b"Error:" in response.data
    assert b"Invalid numeric input" in response.data


def test_form_preserves_all_values(client: FlaskClient) -> None:
    """Test that all form values are preserved after submission.

    Args:
        client: Flask test client.
    """
    form_data = {
        "user_input": "sin(x)",
        "x_min": "-5",
        "x_max": "5",
        "y_min": "-2",
        "y_max": "2",
        "x_name": "Time",
        "y_name": "Amplitude",
        "graph_title": "Sine Wave",
        "x_log": "true",
        "y_log": "true",
    }

    response = client.post("/", data=form_data)
    assert response.status_code == 200

    html_content = response.data.decode()

    # Check that all values are preserved
    assert 'value="sin(x)"' in html_content
    assert 'value="-5"' in html_content
    assert 'value="5"' in html_content
    assert 'value="-2"' in html_content
    assert 'value="2"' in html_content
    assert 'value="Time"' in html_content
    assert 'value="Amplitude"' in html_content
    assert 'value="Sine Wave"' in html_content
    assert "checked" in html_content  # For checkboxes


def test_default_values_populated(client: FlaskClient) -> None:
    """Test that default values are populated on initial load.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200

    html_content = response.data.decode()

    # Check default values
    assert 'value="-10"' in html_content  # x_min default
    assert 'value="10"' in html_content  # x_max default
    assert 'value="x"' in html_content  # x_name default
    assert 'value="y"' in html_content  # y_name default
    assert 'placeholder="Auto"' in html_content  # y_min/y_max placeholders


def test_replot_button_functionality(client: FlaskClient) -> None:
    """Test that the replot button appears after successful plot.

    Args:
        client: Flask test client.
    """
    response = client.post("/", data={"user_input": "x**2"})
    assert response.status_code == 200

    html_content = response.data.decode()
    assert b"Replot with New Settings" in response.data
    assert 'name="action" value="replot"' in html_content


def test_comprehensive_plotting_options(client: FlaskClient) -> None:
    """Test a comprehensive set of plotting options together.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "exp(-x**2) * sin(10*x)",
            "x_min": "-3",
            "x_max": "3",
            "y_min": "-1",
            "y_max": "1",
            "x_name": "Position (cm)",
            "y_name": "Amplitude (V)",
            "graph_title": "Damped Oscillation",
            # No log scales for this test
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_empty_optional_fields(client: FlaskClient) -> None:
    """Test that empty optional fields don't cause errors.

    Args:
        client: Flask test client.
    """
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "y_min": "",  # Empty optional field
            "y_max": "",  # Empty optional field
            "graph_title": "",  # Empty optional field
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data


def test_partial_y_range(client: FlaskClient) -> None:
    """Test setting only y_min or only y_max.

    Args:
        client: Flask test client.
    """
    # Test only y_min
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "y_min": "0",
            "y_max": "",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data

    # Test only y_max
    response = client.post(
        "/",
        data={
            "user_input": "x**2",
            "y_min": "",
            "y_max": "50",
        },
    )
    assert response.status_code == 200
    assert b"Function: y =" in response.data
    assert b"Error:" not in response.data
