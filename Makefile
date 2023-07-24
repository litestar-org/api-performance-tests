.PHONY: install
install:  ## Install all dependencies
	poetry install --extras test --with lint
	pre-commit install

.PHONY: sourcery
sourcery:  ## Run sourcery
	poetry run sourcery review --fix .

.PHONY: tests
test:  ## Run tests
	pytest tests

.PHONY: clean
clean:  ## Remove all generated files
	rm -rf .mypy_cache
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .ruff_cache
	rm -rf results

.PHONY: lint
lint:  ## Run linters
	poetry run pre-commit run --all-files
