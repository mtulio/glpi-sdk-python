PATH_VENV=tests/venv
PATH_VENV_SETUP=$(PATH_VENV)-install
PATH_REQUIREMENTS=tests/requirements.txt

.PHONY: venv
venv:
	rm -rf $(PATH_VENV)
	virtualenv $(PATH_VENV)

.PHONY: dependencies
dependencies:
	@if [ ! -d $(PATH_VENV) ]; then virtualenv $(PATH_VENV) ; fi
	. $(PATH_VENV)/bin/activate && pip install -r $(PATH_REQUIREMENTS)
	. $(PATH_VENV)/bin/activate && pip install --no-cache-dir -e $(PWD)

.PHONY: check-syntax
check-syntax:
	. $(PATH_VENV)/bin/activate && pep8 glpi/*.py

.PHONY: test-setup
test-setup: clean
	@if [ ! -d $(PATH_VENV_SETUP) ]; then virtualenv $(PATH_VENV_SETUP); fi
	. $(PATH_VENV_SETUP)/bin/activate && pip install --no-cache-dir -e $(PWD)

.PHONY: clean
clean:
	@if [ -d $(PATH_VENV) ]; then rm -rf $(PATH_VENV); fi
	@if [ -d $(PATH_VENV_SETUP) ]; then rm -rf $(PATH_VENV_SETUP); fi
