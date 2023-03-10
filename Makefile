.PHONY: help
help: # Display help
	@awk -F ':.*##' '/^[^\t].+?:.*?##/ {printf "\033[36m%-12s\033[0m %s\n", $$1, $$NF}' $(MAKEFILE_LIST)

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
