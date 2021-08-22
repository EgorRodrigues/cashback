export PYTHONPATH=$(shell pwd)/src/
export PYTHONDONTWRITEBYTECODE=1

.PHONY=help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@find . -name ".coverage" | xargs rm -rf
	@find . -name "coverage.xml" | xargs rm -rf


### Dependencies section ###

_base_pip:
	@pip install -U pip poetry wheel

dev-dependencies: _base_pip ## Install development dependencies
	@poetry install

dependencies: _base_pip ## Install dependencies
	@poetry install --no-dev

outdated: ## Show outdated packages
	@poetry show --outdated


### Lint section ###

_flake8:
	@flake8 --show-source src/ tests/

_isort:
	@isort --check-only src/ tests/

_black:
	@black --diff --check src/ tests/

_isort-fix:
	@isort src/ tests/

_black_fix:
	@black src/ tests/

_mypy:
	@mypy src/ tests/

lint: _flake8 _isort _black _mypy  ## Check code lint
format-code: _isort-fix _black_fix  ## Format code


### Tests section ###

test: clean ## Run tests
	@pytest tests/

test-coverage: clean ## Run tests with coverage output
	@pytest tests/ --cov src/ --cov-report term-missing --cov-report xml

test-matching: clean ## Run tests by match ex: make test-matching k=name_of_test
	@pytest -k $(k) tests/


### Run section ###

run:  ## Run server with default settings
	@uvicorn --factory src.main:create_app --reload
