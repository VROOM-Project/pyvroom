help:
		@echo "test      Run test suite"

.PHONY: help test

test:
	python -m black --check src/vroom
	python -m flake8 src/vroom
	python -m mypy src/vroom
	python -m pytest --doctest-modules test src/vroom
