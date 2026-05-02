# Backend dev commands. Run from /backend.

.PHONY: install install-ml dev test lint format check

install:
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -U pip wheel && \
	pip install -e ".[dev]"

install-ml:
	. .venv/bin/activate && pip install -e ".[ml]"

dev:
	. .venv/bin/activate && uvicorn app.main:app --reload --port 8000

test:
	. .venv/bin/activate && pytest -x -v

lint:
	. .venv/bin/activate && ruff check app tests

format:
	. .venv/bin/activate && ruff format app tests

check: lint
	. .venv/bin/activate && mypy app
