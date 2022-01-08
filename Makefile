help:
		@echo "test      Run all tests"
		@echo "develop   Install package in developer mode"
		@echo "format    Format code"


.PHONY: help test develop format

develop:
	python -m pip install -e .

test:
	python -m pytest --doctest-modules test src/vroom
	python -m black --check src/vroom
	python -m flake8 src/vroom
	python -m mypy src/vroom

format:
	@echo format python code with black
	@python -m black src/vroom
	@echo format c++ code with clang-format
	@find src -type f -name '*.cpp' | xargs -I{} clang-format-10 -i -style=file {}
