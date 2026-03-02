help:
		@echo "develop   Install package in developer mode with coverage support"
		@echo "test      Run all tests with coverage (pytest, coverage.py, gcov)"
		@echo "lint      Run all linting (black, flake8, mypy)"
		@echo "format    Format code (black, clang-format-10)"


.PHONY: help test develop format

develop:
	python -m pip install -e .

test:
	coverage run -m pytest --doctest-modules test src/vroom
	mkdir -p coverage
	coverage xml -o coverage/coverage.xml
	GCOV_DIR=$$(find build -maxdepth 2 -type d -name src 2>/dev/null | head -1); \
	gcov -abcfumlpr -o "$$GCOV_DIR" src/_vroom.cpp
	mv *.gcov coverage

lint:
	python -m black --check src/vroom
	python -m flake8 src/vroom
	python -m mypy src/vroom

format:
	@echo format python code with black
	@python -m black src/vroom
	@echo format c++ code with clang-format
	@find src -type f -name '*.cpp' | xargs -I{} clang-format-14 -i -style=file {}
