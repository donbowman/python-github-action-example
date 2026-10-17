.DEFAULT_GOAL := help

.PHONY: help install lock lint format test migrate run docker-build docker-run

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

install: ## Install the project and development dependencies with Poetry
	poetry install

lock: ## Refresh poetry.lock
	poetry lock

lint: ## Check formatting and lint
	poetry run black --check --diff .
	poetry run flake8 .

format: ## Apply formatting
	poetry run black .

test: ## Run the test suite
	poetry run pytest

migrate: ## Apply database migrations
	poetry run alembic upgrade head

run: ## Run the API locally
	poetry run uvicorn example_app.main:app --reload

docker-build: ## Build the container image
	docker build -t python-github-action-example:local .

docker-run: ## Run the container image on port 8000
	docker run --rm -p 8000:8000 -v app-data:/data python-github-action-example:local
