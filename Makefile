.PHONY: all

TMP?=/tmp
INSTALL_DIR?=/opt/goapy
PYTHON_VERSION=3.6.1
PYTHON_INSTALL_FILE=Python-${PYTHON_VERSION}.tar.xz

all: venv

clean:
	rm -rf venv/*

download_interpreter:
	@if [ ! -d python ]; then \
		mkdir ./python; \
	fi
	curl "https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_INSTALL_FILE}" -o ${TMP}/${PYTHON_INSTALL_FILE}
	tar -xf ${TMP}/${PYTHON_INSTALL_FILE} -C ${INSTALL_DIR}/

venv:
	virtualenv -p python3 ${INSTALL_DIR}/venv/
	source venv/bin/activate
	pip install -r requirements

docker:
	echo "Not implemented yet."
