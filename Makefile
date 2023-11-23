init:
	poetry install

run:
	poetry run run-main

lint:
	poetry run black src

test:
	poetry run pytest

typecheck:
	poetry run mypy