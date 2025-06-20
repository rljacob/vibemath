# MathViber 

This repository serves as the starting template for students in the vibe coding class. It contains a short guide of prompts to follow when building a small Flask-based Python package using modern best practices.

By the end of this project, you will have developed a modern Python package named `MathViber` that is capable of:
- Serving a web-based interface using Flask
- Accepting user input for a mathematical expression y = f(x)
- Parsing and plotting the expression over a defined x-range using NumPy and Matplotlib
- Following Python packaging best practices including project structure, dependency management, type checking, linting, CLI setup, and testing

This project demonstrates how to design, build, test, and interact with a real Python package that meets professional standards and is easily extendable for future use.

This guide is part of a hands-on class aimed at teaching how to `vibe` code a  modern Python package that powers a web application. The goal is to give you practical experience with project structure, testing, packaging, and safe web interactivity using Flask and plotting libraries.

You will define a Python package that serves a "Hello, World" page, accepts user input for mathematical functions, and dynamically plots results using Matplotlib and NumPy.

To use this guide on your operating system:
- **Windows**: Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), open Anaconda Prompt or Windows Terminal, then run the `conda` commands as shown.
- **Linux/macOS**: Use Terminal, install Miniconda or Anaconda, and follow the same `conda` instructions.

Make sure to activate your environment with `conda activate mathviber` before running or testing any code.

---

### Notes for Using Cursor

If you're using [Cursor](https://www.cursor.so):

- Open this `PROMPTS.md` file and **only uncomment or copy/paste one prompt at a time**.
- Cursor processes the entire file at once, so avoid having multiple active prompts.
- Alternatively, split each prompt into its own Markdown file under a `/prompts/` folder.
- You can paste prompts directly into Cursor's chat input or click to insert them into your current Python file.

#### Basic Cursor Commands

These prompts are compatible with Cursor's command system. For example:

```cursor
Create a Flask app with a / route that returns 'Hello, World!'
```

```cursor
Generate a test using pytest for the / route of the Flask app.
```

```cursor
Update pyproject.toml to define a CLI script called hello-web
```

Be as specific as possible in your prompt to Cursor. Use clear filenames, functions, and requirements to guide the model.

In addition to the prompts, a `.cursorrules` file is included to configure Cursor with Python best practices.
