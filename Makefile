.PHONY: all

all: venv

clean:
    rm -rf venv/*

venv:
	virtualenv -p python3 venv/
	source venv/bin/activate
	pip install -r requirements

docker:
	echo "Not implemented yet."
