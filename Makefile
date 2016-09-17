.PHONY: all

all: venv

venv:
    virtualenv -p python3 venv/
    source venv/bin/activate
    pip install networkx

docker:
    echo "Not implemented yet."