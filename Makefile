.PHONY: help
help: ## show help
	@grep -h '##\ [[:alnum:]]' $(MAKEFILE_LIST) | sed -E 's/(.*):.*##(.*)/\1: \2/' | column -s: -t

venv: ## create venv
	python3 -m venv venv

.PHONY: install
install: venv ## install/upgrade packaging tools
	venv/bin/pip install --upgrade --upgrade-strategy eager build pip twine

.PHONY: develop
develop: install ## install package in 'development mode'
	venv/bin/python -m pip install -e .

.PHONY: test
test: ## run tests
	venv/bin/pip install --upgrade --upgrade-strategy eager tox
	venv/bin/tox -e py

.PHONY: clean
clean: ## cleanup
	rm -rf .tox
	rm -rf dist
	rm -rf src/*.egg-info
	rm -rf tests/__pycache__

.PHONY: build
build: clean ## build
	venv/bin/python -m build

.PHONY: upload_test
upload_test: build ## upload to https://test.pypi.org
	venv/bin/twine upload --repository testpypi dist/*

.PHONY: upload
upload: build ## upload to https://pypi.org
	venv/bin/twine upload dist/*
