# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from os import path as p
from shutil import rmtree

# Package meta-data.
NAME = 'goap'
DESCRIPTION = 'Goal-Oriented Action Planning implementation in Python. Inspired by Jeff Orkin <>'
URL = 'https://github.com/leopepe/GOApy'
EMAIL = 'lpepefreitas@gmail.com'
AUTHOR = 'Leonardo Pêpe'
LICENSE = 'Simplified BSD License'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = None

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from distutils.core import setup, find_packages, Command


def read(filename, parent=None):
    """
    Args:
        filename:
        parent:
    """
    parent = (parent or __file__)

    try:
        with open(p.join(p.dirname(parent), filename)) as f:
            return f.read()
    except IOError:
        return ''


def parse_requirements(filename, parent=None):
    """
    Args:
        filename:
        parent:
    """
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), filepath):
                yield item
        else:
            yield candidate


requires = list(parse_requirements('requirements.txt'))
# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    VERSION = tuple(list(parse_requirements(os.path.join(here, '.release')))[0].split('=')[-1:][0].split('.'))
    VERSION = '.'.join(map(str, VERSION))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold.

        Args:
            s:
        """
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=requires,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
