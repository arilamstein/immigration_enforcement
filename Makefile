.PHONY: check coverage coverage-html help

check:
	uv run ruff format .
	uv run ruff check .
	uv run mypy .
	uv run pytest tests notebooks/ --nbval-lax

coverage:
	uv run pytest --cov=immigration_enforcement --cov-report=term-missing

coverage-html:
	uv run pytest --cov=immigration_enforcement --cov-report=html
	open htmlcov/index.html

help:
	@echo "Available commands:"
	@echo "  make check          Run all CI checks (linting, type checks, tests)"
	@echo "  make coverage       Run tests with terminal coverage summary"
	@echo "  make coverage-html  Run tests with HTML coverage report and open it"
