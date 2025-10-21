All code in this repo is released under the MIT License. This means that you are free to fork the repository and modify
it to answer whatever questions you have. 

## Installation
I used `uv` to manage my virtual environment while developing this project. To recreate my environment:
1. Clone this repository.
2. Install uv ([link](https://docs.astral.sh/uv/#installation)).
3. In the project directory type `uv sync`. This will create a virtual environment with the project's dependencies in
   `.venv`. 
4. Type `source .venv/bin/activate` to activate the virtual environment.
5. Type `streamlit run streamlit_app.py` to run the app locally.

## App Structure.

The app is built in Python, using the Streamlit and Pandas libraries. 

  * `streamlit_app.py`: Front-end logic and tab layout.
  * `backend.py`: Routes user inputs to the appropriate graphing functions.
  * `detentions.py`: Handles data loading and visualization for the ICE Detentions dataset.
  * `borderpatrol/`: Contains modules for working with Border Patrol Encounters data, including data loading, merging and graph generation.

## CI Checks

This repo has a GitHub Actions workflow that runs `black`, `flake8`, `ruff`, `mypy`, and `pytest` on each pull request. To ensure
your code passes CI, run the following commands from the root directory before submitting a PR:

```bash
uv run black .
uv run flake8 .
uv run ruff check .
uv run mypy .
uv run pytest
```

These commands lint your code, check types, and run all existing tests.

## Code Coverage (Optional)

To generate a code coverage report in the terminal:

```bash
uv run pytest --cov=immigration_enforcement --cov-report=term-missing
```

This gives you a high-level overview of code coverage directly in the terminal. To explore coverage in more
detail—including which lines were missed—run:

```bash
uv run pytest --cov=immigration_enforcement --cov-report=html
open htmlcov/index.html
```