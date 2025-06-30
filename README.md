# MathViber

A modern Python web application for mathematical expression visualization using Flask, NumPy, and Matplotlib.

## Features

- Web-based interface for mathematical expression input
- Real-time plotting of mathematical functions
- Safe expression evaluation with proper input validation
- Modern Python packaging with `src/` layout
- Comprehensive testing and CI/CD pipeline
- Type hints and static analysis
- CLI interface for easy deployment

## Installation

### Using Conda (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mathviber.git
cd mathviber
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate mathviber
```

3. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

### Using pip

```bash
pip install mathviber
```

## Usage

### Command Line Interface

Start the web application:
```bash
mathviber
```

With custom settings:
```bash
mathviber --host 0.0.0.0 --port 8080 --debug
```

### Python API

```python
from mathviber import __version__
print(f"MathViber version: {__version__}")
```

## Development

### Setting up the Development Environment

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

4. Run linting and formatting:
```bash
ruff check .
black .
isort .
flake8 .
mypy src/mathviber/
```

### Project Structure

```
mathviber/
├── src/
│   ├── mathviber/
│   │   ├── __init__.py
│   │   ├── _version.py
│   │   ├── cli.py
│   │   └── py.typed
│   └── tests/
│       ├── __init__.py
│       ├── test_version.py
│       └── test_cli.py
├── pyproject.toml
├── environment.yml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── README.md
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mathviber

# Run specific test file
pytest src/tests/test_version.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Requirements

- Python 3.12+
- Flask 3.0+
- NumPy 1.24+
- Matplotlib 3.7+
- SymPy 1.12+
