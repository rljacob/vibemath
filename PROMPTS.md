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
- Update `.cursorrules` based on this guidelines.
- Do not start building any functionality inside the package on this prompt.
```

### Prompt 0a — Test the Best Practices Setup

```
Verify the package follows Python best practices by checking the following:

1. The folder structure includes:

    MathViber/
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── environment.yml
    ├── pyproject.toml
    ├── src/
    │   └── mathviber/
    │       ├── __init__.py
    │       ├── __version__.py
    │       ├── ...
    │   └── tests/
    │       └── test_example.py

2. `environment.yml` contains dependencies like python=3.12, flask, numpy, matplotlib, pytest, black, isort, flake8, ruff

3. `pyproject.toml` includes:
   - project name "MathViber"
   - version, authors, dependencies
   - `[project.scripts]` section if CLI is used

4. Run:
    conda env create -f environment.yml
    conda activate mathviber
    pip install -e .

5. Linting/formatting checks:
    ruff src/
    flake8 src/
    black --check src/

6. Tests:
    pytest src/

7. Confirm:
   - LICENSE is valid
   - CI file exists or tox.ini is configured
```

---

### Prompt 1 — Create Modern Python Package

```
Create a modern Python package using a `src/` layout. Name the package `hello_webpage`. Set it up with `pyproject.toml` using `setuptools` as the build backend. I want to build a simple Flask web app.

Include:
- `pyproject.toml` with correct metadata (name, version, authors, dependencies)
- `src/hello_webpage/__init__.py`
- `README.md`
- `LICENSE`
- `environment.yml`
- `.gitignore`

Add a test:
- `src/tests/test_structure.py` to assert package import works and metadata exists
```

---

### Prompt 2 — Add Flask App with Homepage

```
Inside `src/hello_webpage/web.py`, create a Flask app with a single route `/` that returns "Hello, World!".

Define:
- `create_app()` to build and return the Flask app
- `main()` to call `create_app().run()`

Add a test:
- `src/tests/test_web_home.py` to verify the route `/` returns HTTP 200 and "Hello, World!" in response
```

---

### Prompt 3 — Add CLI Script Entry Point

```
Update the `pyproject.toml` to include a CLI script called `hello-web` that points to `hello_webpage.web:main`.

Example entry:
[project.scripts]
hello-web = "hello_webpage.web:main"

Add a test:
- `src/tests/test_cli.py` to confirm that running `hello_webpage.web.main()` does not raise and returns a Flask app instance
```

---

### Prompt 4 — Add HTML Input Box and Display Value

```
Update the Flask app to render an HTML page with:
- A text input box
- A button labeled "Input"
- When the user clicks the button, the page should display the submitted text below the form

Use a basic HTML template and handle the form in the Flask route.
```

---

### Prompt 5 — Accept Math Expression and Plot

```
Update the Flask app to:
- Accept a text input like `sin(x)` or `x**2`
- Use `numpy` and `matplotlib` to evaluate and plot `y = f(x)` from x = -10 to 10
- Save the plot to a temporary image file and show it on the webpage after submission

Use `eval` carefully or `numexpr` if needed. Handle simple math functions like sin, cos, log, exp.
```

---

### Prompt 6 — Add a Test for Input and Plot Route

```
Add a test to confirm that the plot route returns 200 and includes a base64 image in response when valid math is submitted.
```

---

### Prompt 7 — Add Dev Tools

```
Add `pytest` as a dev dependency. Also update `pyproject.toml` to configure pytest to look for tests in the `src/` folder.
```

---

Use this sequence to guide yourself or an AI IDE like Cursor from start to finish while learning good structure, safety, and real-world functionality.
