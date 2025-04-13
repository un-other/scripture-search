# scripture-search

A tool for searching scripture.

## Getting started

### Installs

1. Install `pyenv` - [Mac instructions](https://github.com/pyenv/pyenv?tab=readme-ov-file#macos) and get Python 3.12 using `pyenv install 3.12`
2. Install `uv` - [instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation), preferring the standalone installer over using pip.
3. Install the following VS Code / Cursor extensions:
    - "Python" from "ms-python"
    - "Black Formatter" from "ms-python"
    - "isort" from "ms-python"
    - "markdownlint" from "DavidAnson"

### Setting up the environment

1. Create a virtual env with uv using `uv venv`.
    - Make sure the environment is activated in your Cursor/VS Code terminal, for Mac, use `source .venv/bin/activate`
    - Also ensure the environment is being used as the default interpretter for Cursor. Click `Cmd+Shift+P` and type `Python: Select Interpreter` and ensure it's pointing to the local venv at `./.venv/`
2. Install the dependencies using the command `uv sync --extra dev`. This installs all normal dependencies (i.e. `uv sync`) with extra "dev" dependencies (the `--extra dev` part). All dependencies are defined in the `pyproject.toml` file.

### Project structure

The project is organized into several key directories and files:

- `scripture_search/`: The main Python package directory
  - `data_collection/`: Modules for collecting data from various sources
  - `retrievers/`: Modules for retrieving relevant documents (e.g. BM25)
  - `search/`: Modules implementing search methods for taking queries and returning relevant scripture.
  - `config.py`: Configuration settings and constants
  - `logger.py`: Shared logging functionality
  - `main.py`: Run Scripture Search
  - `scripture_types.py`: Pydantic classes for representing scripture

- `notebooks/`: Jupyter notebooks for data analysis and exploration
  - Contains notebooks for data collection, analysis, and visualization
  - Each notebook is dated and describes its specific purpose

- `data/`: Directory for storing collected and processed data
  - Contains raw and processed datasets
  - Used for storing intermediate results during analysis

- `tests/`: Unit tests
  - Contains test files corresponding to the main package modules

- `planning/`: Project planning and documentation
  - Contains design documents, roadmaps, and planning materials
  - Includes ideation documents and project specifications

- `pyproject.toml`: Project configuration and dependency management
  - Defines project metadata and dependencies
  - Used by `uv` for package management

- `.github/`: GitHub-specific configurations
  - Contains GitHub Actions workflows. You can see the workflow runs [here](https://github.com/un-other/scripture-search/actions)
  - Includes PR template.

- `CHANGELOG.md`: Tracks version history and changes
  - Follows Keep a Changelog format
  - Documents all notable changes to the project

### Contributing

1. Don't directly commit into main. Always make a separate branch and then make a Pull Request into main - this keeps our workflow clean and predictable while giving the other person the option to review the PR before merging it. This will also let you verify that the commit passes tests.
