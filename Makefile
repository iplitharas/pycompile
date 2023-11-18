# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

create-env: ## Create python virtual env
	python -m venv .env && source .env/bin/activate && pip install --upgrade pip

poetry-install: create-env ## Create and install environment for local dev
	  source .env/bin/activate && poetry install

package-install: ## Build and install the package
	poetry build && poetry install

install-hooks: ## Install hooks
	pre-commit install

clean-hooks: ## Clean hooks
	pre-commit clean

setup-local-dev: poetry-install install-hooks ## Setup the local environment

test: ## Run locally pytest with coverage
	pytest . -vv -p no:warnings --cov=. --cov-report=xml --cov-report=html

test-local: ## Run pytest with coverage
	pytest . -vv -p no:warnings --cov=.

check: ## Run isort black and pylint in all files
	isort src
	black src
	pylint --recursive y src  --ignore-paths src/examples
	mypy src --exclude src/examples

docs: build-api-docs build-docs  ## Build and server the docs locally
	cd docs && python -m http.server 8083 --directory _build/html

build-api-docs: ## Build api docs
	sphinx-apidoc --output-dir docs src  src/examples/*.py  --separate

build-docs: ## Build docs
	sphinx-build docs docs/_build/html

clean:  ## Clean temp dirs
	rm -rf  .pytest_cache coverage.xml .mypy_cache  .coverage .coverage.* htmlcov

docs: ## Generate docs
	 sphinx-apidoc src --output-dir docs/source_code/ --maxdepth 1 \
     &&  rm -rf docs/_build/* \
 	 && sphinx-build docs docs/_build/html

docs-live: docs  ## Start a local server to render the docs
	 python -m http.server 8091 --directory  docs/_build/html

.PHONY: help create-env poetry-install install-hooks check test package-install \
 		setup-local-dev docs build-api-docs build-docs clean-hooks clean docs docs-live

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)