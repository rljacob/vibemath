**Title: Prompt Guide for Building a Flask-Based Python Package with Input and Plotting Functionality**

---

### Initial Prompt — Python Best Practices

```
I want to build a Python web app using modern best practices. Please follow these guidelines:
- Use the `src/` layout for the package
- Use `pyproject.toml` with PEP 621 and `setuptools`
- Include all dependencies in the appropriate sections
- Keep functions modular, readable, and safe
- Use `pytest` for testing
- Avoid using insecure `eval` unless sandboxed
```

---

### Prompt 1 — Create Modern Python Package

```
Create a modern Python package using a `src/` layout. Name the package `hello_webpage`. Set it up with `pyproject.toml` using `setuptools` as the build backend. I want to build a simple Flask web app.
```

---

### Prompt 2 — Add Flask App with Homepage

```
Inside `src/hello_webpage/web.py`, create a Flask app with a single route `/` that returns "Hello, World!". Also define a `main()` function that runs the app if called.
```

---

### Prompt 3 — Add CLI Script Entry Point

```
Update the `pyproject.toml` to include a CLI script called `hello-web` that points to `hello_webpage.web:main`.
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
Add `pytest` as a dev dependency. Also update `pyproject.toml` to configure pytest to look for tests in the `tests/` folder.
```

---

Use this sequence to guide yourself or an AI IDE like Cursor from start to finish while learning good structure, safety, and real-world functionality.
