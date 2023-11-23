init:
	poetry install

run:
	poetry run run-main

lint:
	poetry run black src

tests:
	poetry run pytest

typecheck:
	poetry run mypy