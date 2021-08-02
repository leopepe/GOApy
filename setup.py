# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from Goap import name, __version__ as version


setup(
    name=name,
    version=version,
    packages=find_packages(),
    url='https://github.com/leopepe/GOApy',
    license='Simplified BSD License',
    author='Leonardo Pêpe',
    author_email='lpepefreitas@gmail.com',
    description='Goal-Oriented Action Planning implementation in Python. Inspired by Jeff Orkin GOAP <http://alumni.media.mit.edu/~jorkin/goap.html>',
    test_suite='tests',
    python_requires='>=3.0',
)
