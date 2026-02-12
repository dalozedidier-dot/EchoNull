PYTHON ?= python

.PHONY: install lint format type test build sweep doctor

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check src tests
	black --check src tests
	mypy src tests

format:
	ruff check src tests --fix
	black src tests

type:
	mypy src tests

test:
	pytest -q --cov=echonull --cov-report=term-missing:skip-covered --cov-fail-under=100

build:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*

sweep:
	$(PYTHON) -m echonull.orchestrator.run --runs 5 --out _ci_out --workers 2 --zip

doctor:
	echonull-doctor
