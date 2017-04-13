PATH_VENV=tests/venv
PATH_REQUIREMENTS=tests/requirements.txt
VENV_ACTIVATE=". $(PATH_VENV)/bin/activate"

.PHONY: venv
venv:
	rm -rf $(PATH_VENV)
	virtualenv $(PATH_VENV)

.PHONY: dependencies
dependencies:
	@if [ ! -d $(PATH_VENV) ]; then virtualenv $(PATH_VENV) ; fi
	. $(PATH_VENV)/bin/activate && pip install -r $(PATH_REQUIREMENTS)

.PHONY: check-syntax
check-syntax:
	. $(PATH_VENV)/bin/activate && pep8 *.py
