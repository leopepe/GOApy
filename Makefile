REGISTRY_HOST=docker.io
USERNAME=$(USER)
NAME=$(shell basename $(PWD))

RELEASE_SUPPORT := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))/.make-release-support
IMAGE=$(shell tr '[:upper:]' '[:lower:]' <<< $(NAME))

VERSION=$(shell . $(RELEASE_SUPPORT) ; getVersion)
TAG=$(shell . $(RELEASE_SUPPORT); getTag)

SHELL=/bin/bash

PYTHON_VERSION=3.7

.PHONY: all

all: help #docker-build container-run

# Show this help.
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

docker-all: pre-build docker-build post-build build release patch-release minor-release major-release tag check-status check-release showver \
	push do-push post-push

# builds a new version of your Docker image and tags it
build: pre-build docker-build post-build

pre-build:

post-build:

post-push:

container-run:
	@echo "Go Go Go..."
	docker run -it --rm $(IMAGE):$(VERSION) /bin/bash

docker-build: .release
	docker build -t $(IMAGE):$(VERSION) .
	@DOCKER_MAJOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f1) ; \
	DOCKER_MINOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f2) ; \
	if [ $$DOCKER_MAJOR -eq 1 ] && [ $$DOCKER_MINOR -lt 10 ] ; then \
		echo docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
	else \
		echo docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ; \
	fi

.release:
	@echo "release=0.0.0" > .release
	@echo "tag=$(NAME)-0.0.0" >> .release
	@echo INFO: .release created
	@cat .release

# build the current release and push the image to the registry
release: check-status check-release  #push

push: build do-push post-push

do-push: 
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

# build from the current (dirty) workspace and pushes the image to the registry
snapshot: build push

# will show the current release tag based on the directory content.
showver: .release
	@. $(RELEASE_SUPPORT); getVersion

tag-patch-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextPatchLevel)
tag-patch-release: .release tag

tag-minor-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextMinorLevel)
tag-minor-release: .release tag 

tag-major-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextMajorLevel)
tag-major-release: .release tag 

# Increments the patch release level, build and push to git
patch-release: tag-patch-release release
	@echo $(VERSION)

# increments the minor release level, build and push to git
minor-release: tag-minor-release release
	@echo $(VERSION)

# increments the major release level, build and push to registry
major-release: tag-major-release release
	@echo $(VERSION)


tag: TAG=$(shell . $(RELEASE_SUPPORT); getTag $(VERSION))
tag: check-status
	@. $(RELEASE_SUPPORT) ; ! tagExists $(TAG) || (echo "ERROR: tag $(TAG) for version $(VERSION) already tagged in git" >&2 && exit 1) ;
	@. $(RELEASE_SUPPORT) ; setRelease $(VERSION)
	git add .release
	git commit -m "bumped to version $(VERSION)" ;
	git tag $(TAG) ;
	@[ -n "$(shell git remote -v)" ] && git push --tags

# will check whether there are outstanding changes
check-status:
	@. $(RELEASE_SUPPORT) ; ! hasChanges || (echo "ERROR: there are still outstanding changes" >&2 && exit 1) ;

# will check whether the current directory matches the tagged release in git.
check-release: .release
	@. $(RELEASE_SUPPORT) ; tagExists $(TAG) || (echo "ERROR: version not yet tagged in git. make [minor,major,patch]-release." >&2 && exit 1) ;
	@. $(RELEASE_SUPPORT) ; ! differsFromRelease $(TAG) || (echo "ERROR: current directory differs from tagged $(TAG). make [minor,major,patch]-release." ; exit 1)

# Create VirtualEnv venv
venv:
	python3.7 -m venv venv/
	source venv/bin/activate

# Install GOApy
install-in-venv: venv
	venv/bin/python setup.py install

# upload tag
upload: venv
	venv/bin/python setup.py upload

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

# Clean all
clean: venv clean-pyc
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

