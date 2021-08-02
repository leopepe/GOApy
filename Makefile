.PHONY: all

REGISTRY_HOST=docker.io
USERNAME=$(USER)
NAME=$(shell basename $(PWD))

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
IMAGE=$(shell tr '[:upper:]' '[:lower:]' <<< $(NAME))

VERSION=$(shell poetry version|cut -d" " -f2)

SHELL=/bin/bash

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
	@echo "Installing Python version ${PYTHON_VERSION}"
	pyenv install ${PYTHON_VERSION}
endif
	pyenv local ${PYTHON_VERSION}
	pip install poetry virtualenv

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
	@poetry version|cut -d" " -f2 > ./VERSION && echo $(shell cat ./VERSION)

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
	python setup.py install

format: venv
	autopep8 --in-place --aggressive --aggressive --aggressive --recursive Goap/

install-in-venv: venv install
	python setup.py install

unittest: install-in-venv
	echo "Action Class Unittests"
	pytest -v tests/Action_test.py
	echo "Sensor Class Unittests"
	pytest -v tests/Sensor_test.py
	echo "Automaton Class Unittests"
	pytest -v tests/Automaton_test.py
	echo "Fullstack Unittests"
	pytest -v tests/Planner_test.py

install-coveralls: venv install-in-venv
	pip install coveralls

test-coverage: install-coveralls
	coverage run --source=Goap/ setup.py test

docker-build:
	docker build -t goapy:$(shell poetry version|cut -d" " -f2) .

clean-venv:
	rm -rf .venv/

clean-build:
	rm -rf build/ *.egg-info/

clean-all: clean-venv clean-build

clean: clean-all
