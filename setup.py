# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import Goap


setup(
    name=Goap.__name__,
    version=Goap.__version__,
    packages=find_packages(),
    url='',
    license='Simplified BSD License',
    author='Leonardo Pêpe',
    author_email='lpepefreitas@gmail.com',
    description='Goal-Oriented Action Planning implementation in Python. Inspired by Jeff Orkin <>',
    test_suite='tests',
)
