**Title: Prompt Guide for Building a Flask-Based Python Package with Input and Plotting Functionality**

---

### Prompt 0 — Python Best Practices

```
I want to build a Python web app using modern best practices. Please follow these guidelines:
- Python version should be 3.12
- My package will be called "MathViber"
- Use the `src/` layout for the package
- Use `pyproject.toml` with PEP 621 and `setuptools`
- Include all dependencies in the appropriate sections
- Keep functions modular, readable, and safe
- Use `pytest` for testing
- Place all tests inside the `src/` folder
- Avoid using insecure `eval` unless sandboxed
- Add a `README.md` with usage instructions
- Add a `LICENSE` file (e.g., MIT)
- Add `.gitignore` to exclude `__pycache__`, `.conda`, `.ipynb_checkpoints`, and build files
- Add `__version__` inside the package for tracking
- Include type hints and configure linting (e.g., `ruff`, `flake8`)
- Set up basic CI (e.g., GitHub Actions or `tox`) to run tests automatically
- Optionally configure formatting tools (e.g., `black`, `isort`)
- Use `conda` for environment and dependency management instead of `venv`
- Install `pre-commit` and set up `.pre-commit-config.yaml` to run: `ruff`, `black`, `isort`, `flake8`, `pytest`
- Update `.cursorrules` based on this guidelines and python best practices.
- Do not start building any functionality inside the package on this prompt.
- Avoid creating unnecessary files and folders (e.g., Makefiles, scripts, notebooks) unless strictly needed later.
- Avoid creating scaffolding folders inside the package until necessary.
```

### Prompt 0a — Test the Best Practices Setup

```
Verify that the MathViber package is properly scaffolded:

- Check that the project has `README.md`, `LICENSE`, `environment.yml`, `.gitignore`, and `pyproject.toml`
- Confirm `src/mathviber/` exists with `__init__.py` and `__version__.py`
- Ensure `src/tests/` exists with one example test
- Check Python version is 3.12 and required dependencies are in `environment.yml`
- Run `conda env create -f environment.yml` and `pip install -e .`
- Run `pre-commit run --all-files`
```

### Prompt 1 — Scaffold Package and Add Homepage

```
Check if the minimal Flask app defines a homepage that can be tested.

The app needs to have defined:
- `create_app()` to build and return the Flask app
- A route `/` that returns "Hello, World!"
- `main()` that runs the app

Tests:
- `src/tests/test_structure.py`: check import and metadata presence
- `src/tests/test_app_home.py`: check `/` returns HTTP 200 and contains "Hello, World!"
- Correct entry on `pyproject.toml` for the CLI. 
- `src/tests/test_cli.py`: confirm `main()` runs without errors and returns a Flask app
```

### Prompt 1a — Check That It Works

```
Run the following to validate setup and functionality:

1. Create and activate environment
2. Install package
3. Run app
4. Test and lint

Ensure all tests pass and app is accessible at http://127.0.0.1:5000/ with "Hello, World!"
```


### Prompt 2 — Add HTML Input Box and Display Value

```
Update the Flask app to render an HTML page with:
- A text input box
- A button labeled "Input"
- When the user clicks the button, the page should display the submitted text below the form

Use a basic HTML template and handle the form in the Flask route.
```


### Prompt 3 — Accept Math Expression and Plot

```
Update the Flask app to:
- Accept a text input like `sin(x)` or `x**2`
- Check if the input is a valid mathematical formula
- Keep the input on the text input when the button is pressed
- Add an example text to the text input
- Use `numpy` and `matplotlib` to evaluate and plot `y = f(x)` from x = -10 to 10
- Save the plot to a temporary image file and show it on the webpage after submission
- Add a button to download the plot
```


### Prompt 4 — Customization

```
- Add inputs for x_max, x_min, y_max, y_man
- Add checkbox for x_log, y_log
- Add input names for the graph, x_name, y_name
- Prepopulate the inputs
- Add a button to plot the graph again
```

### Prompt 5 — Interactive plots!

```
- Make the plot interactive by using plotly
- Make sure the graph updates when new values are added on the input boxes
- Make sure the download button is still working
```
