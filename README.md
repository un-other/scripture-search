# scripture-search

A tool for searching scripture.

## Getting started

### Installs

1. Install `pyenv` - [Mac instructions](https://github.com/pyenv/pyenv?tab=readme-ov-file#macos) and get Python 3.12 using `pyenv install 3.12`
2. Install `uv` - [instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation), preferring the standalone installer over using pip.

### Setting up the environment

1. Create a virtual env with uv using `uv venv`.
    - Make sure the environment is activated in your Cursor/VS Code terminal, for Mac, use `source .venv/bin/activate`
    - Also ensure the environment is being used as the default interpretter for Cursor. Click `Cmd+Shift+P` and type `Python: Select Interpreter` and ensure it's pointing to the local venv at `./.venv/`
2. Install the dependencies using the command `uv pip install -e ".[dev]"`. This installs all normal dependencies (i.e. `uv pip install`) with extra "dev" dependencies (the `-e ".[dev]"` part). All dependencies are defined in the `pyproject.toml` file.
