PYTHON = python3
SRC = src tests

format:
	@echo "Formatting code with Black..."
	black $(SRC)

test:
	@echo "Running Pytest..."
	PYTHONPATH=$(PWD) pytest -v

check:
	@echo "Running formatting and tests..."
	make format
	make test
	@echo "All checks passed successfully."

clean:
	@echo "Cleaning cache and build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache build dist