VENV=venv

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

PYTHON=$(VENV_BIN)/python
PYTEST=$(VENV_BIN)/pytest

.PHONY: build
build:
	$(PYTHON) -m build

.PHONY: clean
clean:
	rm -rf dist

.PHONY: dev-setup
dev-setup: venv dev-requirements

.PHONY: venv
venv:
	python -m venv $(VENV)

.PHONY: dev-requirements
dev-requirements: dev-requirements.txt
	$(PYTHON) -m pip install -r dev-requirements.txt

.PHONY: test
test:
	$(PYTEST)

.PHONY: upload-pypi
upload-pypi:
	$(PYTHON) -m twine upload --verbose dist/*

.PHONY: release
release: clean build upload-pypi

.PHONY: ci
ci: dev-setup test build