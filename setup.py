# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import Goap


setup(
    name=Goap.__name__,
    version=Goap.__version__,
    packages=find_packages(),
    url='https://github.com/leopepe/GOApy',
    license='Simplified BSD License',
    author='Leonardo Pêpe',
    author_email='lpepefreitas@gmail.com',
    description='Goal-Oriented Action Planning implementation in Python. Inspired by Jeff Orkin GOAP <>',
    test_suite='tests',
)
