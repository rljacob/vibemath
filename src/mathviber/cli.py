"""Command-line interface for MathViber."""

import argparse

from mathviber._version import __version__


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="mathviber",
        description="MathViber: Mathematical expression visualization web app",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"MathViber {__version__}",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind the server to (default: 5000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    args = parser.parse_args(argv)

    # Import and run the Flask app
    from mathviber.app import main as flask_main

    app = flask_main()
    print(f"MathViber {__version__} starting on {args.host}:{args.port}")
    if args.debug:
        print("Debug mode enabled")

    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    exit(main())
