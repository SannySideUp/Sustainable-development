PYTHON = python3
SRC = src tests

format:
	@echo "Formatting code with Black..."
	black $(SRC)

test:
	@echo "Running Pytest..."
	PYTHONPATH="$(PWD)" pytest -v

check:
	@echo "Running formatting and tests..."
	make test
	@echo "All checks passed successfully."

clean:
	@echo "Cleaning cache and build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache build dist

.PHONY: doc uml

doc:
	sphinx-apidoc -o doc/api .
	make -C doc/api html

uml:
	@echo "Generating UML diagrams..."
	mkdir -p doc/uml
	pyreverse -o png -p SustainableDevelopment src
	mv classes_SustainableDevelopment.png doc/uml/
	mv packages_SustainableDevelopment.png doc/uml/
	@echo "UML diagrams generated in doc/uml/"