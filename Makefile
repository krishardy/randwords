VENV=venv
VENV_SCRIPTS=$(VENV)/Scripts
PYTHON=$(VENV_SCRIPTS)/python

.PHONY: build
build:
	$(PYTHON) -m build

.PHONY: clean
clean:
	rm -rf dist

.PHONY: dev-setup
dev-setup: dev-requirements.txt
	python -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r dev-requirements.txt

.PHONY: test
test:

.PHONY: upload-pypi
upload-pypi:
	$(PYTHON) -m twine upload --verbose dist/*