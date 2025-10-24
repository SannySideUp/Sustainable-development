SRC      ?= src
TESTS    ?= tests
VENV     ?= .venv
DOC_DIR  ?= doc
API_DIR  ?= $(DOC_DIR)/api

ifeq ($(OS),Windows_NT)
SHELL := cmd
.SHELLFLAGS := /C
SYS_PY := python
PY  := $(VENV)\Scripts\python.exe
PIP := $(VENV)\Scripts\pip.exe
else
SHELL := /bin/bash
.SHELLFLAGS := -c
SYS_PY := python3
PY  := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
endif

.PHONY: venv install run test clean format doc serve-doc

venv:
ifeq ($(OS),Windows_NT)
	if not exist "$(PY)" ( $(SYS_PY) -m venv "$(VENV)" )
else
	[ -x "$(PY)" ] || $(SYS_PY) -m venv "$(VENV)"
endif
	"$(PIP)" install -U pip

install: venv
	"$(PIP)" install -r requirements.txt

run:
	"$(PY)" main.py

test:
	PYTHONPATH="$(PWD)" pytest -v

format:
	"$(PIP)" install black
	"$(PY)" -m black $(SRC) $(TESTS) main.py

uml:
	@echo "Generating UML diagrams..."
	mkdir -p doc/uml
	pyreverse -o png -p SustainableDevelopment src
	mv classes_SustainableDevelopment.png doc/uml/
	mv packages_SustainableDevelopment.png doc/uml/
	@echo "UML diagrams generated in doc/uml/"

doc:
	"$(PIP)" install pdoc
	"$(PY)" -c "import os; os.makedirs(r'$(API_DIR)', exist_ok=True)"
	"$(PY)" -m pdoc --output-dir "$(API_DIR)" --docformat google --no-show-source "$(SRC)"
	@echo "✓ Documentation generated in $(API_DIR)/"

serve-doc:
	"$(PIP)" install pdoc
	@echo "Serving docs at http://localhost:8080 — press Ctrl+C to stop"
	"$(PY)" -m pdoc "$(SRC)" -h localhost -p 8080 --docformat google --no-show-source

clean:
	"$(PY)" -c "import shutil, pathlib; \
[shutil.rmtree(pathlib.Path(p), ignore_errors=True) for p in ['__pycache__','.pytest_cache','htmlcov','$(API_DIR)']]; \
print('✓ Cleaned build/test artifacts')"

quality:
	@echo "Running pylint..."
	- "$(PY_ABS)" -m pylint --exit-zero --recursive=y "$(SRC)"
	@echo "Running tests with coverage..."
	"$(PY)" -m pytest "$(TESTS)" \
		--maxfail=1 \
		--cov="$(SRC)" \
		--cov-report=term-missing
	@echo "✓ Quality check finished"
