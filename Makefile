check:
	uv run black .
	uv run flake8 .
	uv run ruff check .
	uv run mypy .
	uv run pytest

coverage:
	uv run pytest --cov=immigration_enforcement --cov-report=html
	open htmlcov/index.html
