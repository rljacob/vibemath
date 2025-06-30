"""Flask application factory and routes for MathViber."""

import os
import tempfile
import uuid

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, jsonify, render_template, request, send_file


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Store plot files in a temporary directory
    plot_dir = tempfile.mkdtemp(prefix="mathviber_plots_")

    def validate_and_evaluate_expression(
        expression: str, x_min: float = -10, x_max: float = 10, num_points: int = 1000
    ) -> tuple[bool, str | None, np.ndarray | None, np.ndarray | None]:
        """Validate and evaluate a mathematical expression safely.

        Args:
            expression: The mathematical expression to evaluate.
            x_min: Minimum x value for evaluation.
            x_max: Maximum x value for evaluation.
            num_points: Number of points to evaluate.

        Returns:
            Tuple of (is_valid, error_message, x_values, y_values).
        """
        # Define allowed functions and constants
        allowed_names = {
            "x": None,  # Will be replaced with actual x values
            "pi": np.pi,
            "e": np.e,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "log10": np.log10,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pow": np.power,
            "sinh": np.sinh,
            "cosh": np.cosh,
            "tanh": np.tanh,
            "arcsin": np.arcsin,
            "arccos": np.arccos,
            "arctan": np.arctan,
        }

        try:
            # Create x values from x_min to x_max
            if x_min >= x_max:
                return False, "X minimum must be less than X maximum", None, None
            x = np.linspace(x_min, x_max, num_points)

            # Replace ** with np.power for safety and x with actual values
            safe_expression = expression.replace("**", "^")

            # Check for dangerous operations
            dangerous_ops = ["import", "exec", "eval", "open", "file", "__"]
            if any(op in expression.lower() for op in dangerous_ops):
                return False, "Expression contains forbidden operations", None, None

            # Prepare the namespace for evaluation
            namespace = dict(allowed_names)
            namespace["x"] = x

            # Replace ^ with ** for numpy power operations
            safe_expression = safe_expression.replace("^", "**")

            # Evaluate the expression
            try:
                y = eval(safe_expression, {"__builtins__": {}}, namespace)

                # Ensure y is a numpy array
                if not isinstance(y, np.ndarray):
                    y = np.full_like(x, y)

                return True, None, x, y

            except Exception as e:
                return False, f"Error evaluating expression: {str(e)}", None, None

        except Exception as e:
            return False, f"Error processing expression: {str(e)}", None, None

    def create_interactive_plot(
        expression: str,
        x: np.ndarray,
        y: np.ndarray,
        x_name: str = "x",
        y_name: str = "y",
        graph_title: str = "",
        x_log: bool = False,
        y_log: bool = False,
        y_min: float | None = None,
        y_max: float | None = None,
    ) -> tuple[str, str]:
        """Create an interactive Plotly plot.

        Args:
            expression: The mathematical expression.
            x: X values.
            y: Y values.
            x_name: Label for x-axis.
            y_name: Label for y-axis.
            graph_title: Title for the graph.
            x_log: Whether to use logarithmic scale for x-axis.
            y_log: Whether to use logarithmic scale for y-axis.
            y_min: Minimum y value for plot range.
            y_max: Maximum y value for plot range.

        Returns:
            Tuple of (plot_html, plot_id).
        """
        # Create the plot
        fig = go.Figure()

        # Add the main trace
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"{y_name} = {expression}",
                line=dict(color="#2196F3", width=2),
                hovertemplate=f"<b>{x_name}:</b> %{{x}}<br><b>{y_name}:</b> %{{y}}<extra></extra>",
            )
        )

        # Set title
        title = graph_title if graph_title else f"{y_name} = {expression}"

        # Configure layout
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16, family="Arial")),
            xaxis_title=x_name,
            yaxis_title=y_name,
            font=dict(family="Arial", size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=60, r=60, t=60, b=60),
            height=500,
        )

        # Set axis types and ranges
        xaxis_type = "log" if x_log else "linear"
        yaxis_type = "log" if y_log else "linear"

        fig.update_xaxes(
            type=xaxis_type,
            gridcolor="lightgray",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="black",
            zerolinewidth=1,
        )

        # Set y-axis range
        y_range = None
        if y_min is not None and y_max is not None:
            y_range = [y_min, y_max]
        elif y_min is not None or y_max is not None:
            finite_y = y[np.isfinite(y)]
            if len(finite_y) > 0:
                auto_y_min, auto_y_max = np.percentile(finite_y, [5, 95])
                y_range = [
                    y_min if y_min is not None else auto_y_min,
                    y_max if y_max is not None else auto_y_max,
                ]

        fig.update_yaxes(
            type=yaxis_type,
            gridcolor="lightgray",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="black",
            zerolinewidth=1,
            range=y_range,
        )

        # Generate plot HTML and unique ID
        plot_id = f"plot_{uuid.uuid4().hex}"
        plot_html = pio.to_html(
            fig,
            include_plotlyjs="cdn",
            div_id=plot_id,
            config={
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadSvg"],
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": "mathviber_plot",
                    "height": 500,
                    "width": 800,
                    "scale": 2,
                },
            },
        )

        return plot_html, plot_id

    def create_static_plot_for_download(
        expression: str,
        x: np.ndarray,
        y: np.ndarray,
        x_name: str = "x",
        y_name: str = "y",
        graph_title: str = "",
        x_log: bool = False,
        y_log: bool = False,
        y_min: float | None = None,
        y_max: float | None = None,
    ) -> str:
        """Create a static plot for download purposes.

        Args:
            expression: The mathematical expression.
            x: X values.
            y: Y values.
            x_name: Label for x-axis.
            y_name: Label for y-axis.
            graph_title: Title for the graph.
            x_log: Whether to use logarithmic scale for x-axis.
            y_log: Whether to use logarithmic scale for y-axis.
            y_min: Minimum y value for plot range.
            y_max: Maximum y value for plot range.

        Returns:
            The filename of the saved plot.
        """
        # Create the same plot as interactive but save as static image
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"{y_name} = {expression}",
                line=dict(color="#2196F3", width=2),
            )
        )

        title = graph_title if graph_title else f"{y_name} = {expression}"

        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            xaxis_title=x_name,
            yaxis_title=y_name,
            font=dict(size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            width=800,
            height=500,
        )

        # Set axis types and ranges (same as interactive plot)
        xaxis_type = "log" if x_log else "linear"
        yaxis_type = "log" if y_log else "linear"

        fig.update_xaxes(type=xaxis_type, gridcolor="lightgray", zeroline=True)

        y_range = None
        if y_min is not None and y_max is not None:
            y_range = [y_min, y_max]
        elif y_min is not None or y_max is not None:
            finite_y = y[np.isfinite(y)]
            if len(finite_y) > 0:
                auto_y_min, auto_y_max = np.percentile(finite_y, [5, 95])
                y_range = [
                    y_min if y_min is not None else auto_y_min,
                    y_max if y_max is not None else auto_y_max,
                ]

        fig.update_yaxes(
            type=yaxis_type, gridcolor="lightgray", zeroline=True, range=y_range
        )

        # Save as PNG
        filename = f"plot_{uuid.uuid4().hex}.png"
        filepath = os.path.join(plot_dir, filename)
        fig.write_image(filepath, width=800, height=500, scale=2)

        return filename

    @app.route("/", methods=["GET", "POST"])
    def home() -> str:
        """Home page route with mathematical expression handling.

        Returns:
            str: Rendered HTML template.
        """
        submitted_text = None
        error_message = None
        plot_filename = None

        if request.method == "POST":
            submitted_text = request.form.get("user_input", "").strip()

            if submitted_text:
                # Get plotting parameters from form
                try:
                    x_min = float(request.form.get("x_min", -10))
                    x_max = float(request.form.get("x_max", 10))

                    # Optional y limits
                    y_min_str = request.form.get("y_min", "").strip()
                    y_max_str = request.form.get("y_max", "").strip()
                    y_min = float(y_min_str) if y_min_str else None
                    y_max = float(y_max_str) if y_max_str else None

                    # Axis labels and title
                    x_name = request.form.get("x_name", "x").strip() or "x"
                    y_name = request.form.get("y_name", "y").strip() or "y"
                    graph_title = request.form.get("graph_title", "").strip()

                    # Log scale options
                    x_log = request.form.get("x_log") == "true"
                    y_log = request.form.get("y_log") == "true"

                    # Validate and evaluate the expression
                    is_valid, error, x_vals, y_vals = validate_and_evaluate_expression(
                        submitted_text, x_min, x_max
                    )

                    if is_valid and x_vals is not None and y_vals is not None:
                        # Create interactive plot
                        try:
                            plot_html, plot_id = create_interactive_plot(
                                submitted_text,
                                x_vals,
                                y_vals,
                                x_name=x_name,
                                y_name=y_name,
                                graph_title=graph_title,
                                x_log=x_log,
                                y_log=y_log,
                                y_min=y_min,
                                y_max=y_max,
                            )
                            # Also create static plot for download
                            plot_filename = create_static_plot_for_download(
                                submitted_text,
                                x_vals,
                                y_vals,
                                x_name=x_name,
                                y_name=y_name,
                                graph_title=graph_title,
                                x_log=x_log,
                                y_log=y_log,
                                y_min=y_min,
                                y_max=y_max,
                            )
                        except Exception as e:
                            error_message = f"Error creating plot: {str(e)}"
                            plot_html = None
                            plot_id = None
                    else:
                        error_message = error

                except ValueError as e:
                    error_message = f"Invalid numeric input: {str(e)}"
                except Exception as e:
                    error_message = f"Error processing form data: {str(e)}"

        return render_template(
            "index.html",
            submitted_text=submitted_text,
            error_message=error_message,
            plot_filename=plot_filename,
            plot_html=plot_html if "plot_html" in locals() else None,
            plot_id=plot_id if "plot_id" in locals() else None,
        )

    @app.route("/plot/<filename>")
    def plot_image(filename: str):
        """Serve plot image files.

        Args:
            filename: The filename of the plot image.

        Returns:
            The plot image file.
        """
        filepath = os.path.join(plot_dir, filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype="image/png")
        else:
            return "Plot not found", 404

    @app.route("/download/<filename>")
    def download_plot(filename: str):
        """Download plot image files.

        Args:
            filename: The filename of the plot image.

        Returns:
            The plot image file as download.
        """
        filepath = os.path.join(plot_dir, filename)
        if os.path.exists(filepath):
            return send_file(
                filepath,
                mimetype="image/png",
                as_attachment=True,
                download_name="mathviber_plot.png",
            )
        else:
            return "Plot not found", 404

    @app.route("/api/update_plot", methods=["POST"])
    def update_plot():
        """API endpoint for real-time plot updates.

        Returns:
            JSON response with plot HTML or error message.
        """
        try:
            data = request.get_json()
            expression = data.get("expression", "").strip()

            if not expression:
                return jsonify({"error": "No expression provided"})

            # Get plotting parameters
            x_min = float(data.get("x_min", -10))
            x_max = float(data.get("x_max", 10))

            y_min_str = data.get("y_min", "")
            y_max_str = data.get("y_max", "")
            y_min = float(y_min_str) if y_min_str else None
            y_max = float(y_max_str) if y_max_str else None

            x_name = data.get("x_name", "x") or "x"
            y_name = data.get("y_name", "y") or "y"
            graph_title = data.get("graph_title", "")

            x_log = data.get("x_log", False)
            y_log = data.get("y_log", False)

            # Validate and evaluate the expression
            is_valid, error, x_vals, y_vals = validate_and_evaluate_expression(
                expression, x_min, x_max
            )

            if is_valid and x_vals is not None and y_vals is not None:
                # Create interactive plot
                plot_html, plot_id = create_interactive_plot(
                    expression,
                    x_vals,
                    y_vals,
                    x_name=x_name,
                    y_name=y_name,
                    graph_title=graph_title,
                    x_log=x_log,
                    y_log=y_log,
                    y_min=y_min,
                    y_max=y_max,
                )

                # Create static plot for download
                plot_filename = create_static_plot_for_download(
                    expression,
                    x_vals,
                    y_vals,
                    x_name=x_name,
                    y_name=y_name,
                    graph_title=graph_title,
                    x_log=x_log,
                    y_log=y_log,
                    y_min=y_min,
                    y_max=y_max,
                )

                return jsonify(
                    {
                        "success": True,
                        "plot_html": plot_html,
                        "plot_id": plot_id,
                        "plot_filename": plot_filename,
                    }
                )
            else:
                return jsonify({"error": error})

        except ValueError as e:
            return jsonify({"error": f"Invalid numeric input: {str(e)}"})
        except Exception as e:
            return jsonify({"error": f"Error processing request: {str(e)}"})

    # Cleanup function for temporary files (optional)
    @app.teardown_appcontext
    def cleanup_temp_files(error):
        """Clean up temporary files when app context ends."""
        # This is a basic cleanup - in production you might want more sophisticated cleanup
        pass

    return app


def main() -> Flask:
    """Create and return the Flask app for CLI usage.

    Returns:
        Flask: Flask application instance.
    """
    return create_app()
