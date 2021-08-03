.PHONY: all

REGISTRY_HOST=docker.io
USERNAME=$(USER)
NAME=$(shell basename $(PWD))

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
IMAGE=$(shell tr '[:upper:]' '[:lower:]' <<< $(NAME))

VERSION=$(shell poetry version|cut -d" " -f2)

SHELL=/bin/bash

# the python version must be inline with:
# * poetry, travis, docker
PYTHON_VERSION=3.8.5
PYTHON_MINOR_VERSION=3.8

all: venv install-in-venv test

test: unittest test-coverage

req:
ifeq ($(shell which pyenv), "pyenv not found")
	@echo "Installing pyenv"
	curl https://pyenv.run | bash
endif
ifneq ($(shell python --version|cut -d" " -f2), ${PYTHON_VERSION})
ifeq ("v$(shell pyenv versions|grep ${PYTHON_VERSION}|cut -d' ' -f2)", "v${PYTHON_VERSION}")
	@echo "Local python version must be ${PYTHON_VERSION}"
	pyenv local ${PYTHON_VERSION}
else
	@echo "Python ${PYTHON_VERSION} not in local pyenv versions. Installing python ${PYTHON_VERSION}"
	pyenv install ${PYTHON_VERSION}
	pyenv local ${PYTHON_VERSION}
	pip install poetry virtualenv
endif
endif

patch:
	poetry version patch
	poetry version|cut -d" "  -f2 > .release

minor:
	poetry version minor 
	poetry version|cut -d" "  -f2 > .release

major:
	poetry version major
	poetry version|cut -d" "  -f2 > .release

.PHONY: version
version:
	@poetry version|cut -d" " -f2

release-minor: minor tag

tag: TAG=$(shell cat .release)
tag: check-status
	REL=$(shell cat .release)
	HASTAG=$(shell git tag -l |grep ^"v${REL}\$")
	@test "$(BRACH)" = "mater" || (echo "ERROR: Please merge your changes to master first" >&2 && exit 1)
	@test -n "$tag" && test -z "$(HASTAG)" || (echo "ERROR: Tag already exists" >&2 && exit 1)
	git tag v$(TAG)
	@[ -n "$(shell git remote -v)" ] && git push --tags

check-status:
	test -n "$(git status -s .)" || (echo "ERROR: there are still outstanding changes" >&2 && exit 1) ;

venv: req
	poetry install

install:
	poetry run python setup.py install

lint: format
	poetry run flake8 goap/

format: venv
	autopep8 --in-place --aggressive --aggressive --aggressive --recursive goap/

install-in-venv: venv install
	poetry run python setup.py install

unittest: install-in-venv
	@echo "Running unit tests"
	poetry run pytest -v -s tests/

test-coverage: venv
	poetry run coverage run --source=goap/ setup.py test

docker-build:
	docker build -t goapy:$(shell poetry version|cut -d" " -f2) .

clean-venv:
	rm -rf .venv/

clean-build:
	rm -rf build/ *.egg-info/

clean-dist:
	rm -rf dist/

clean-all: clean-venv clean-build clean-dist

clean: clean-all
