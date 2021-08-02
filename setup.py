# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from Goap import name, __version__ as version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=name,
    version=version,
    packages=find_packages(),
    url='https://github.com/leopepe/GOApy',
    project_urls={
        "Bug Tracker": "https://github.com/leopepe/GOApy/issues",
    },
    license='Simplified BSD License',
    author='Leonardo Pêpe de Freitas',
    author_email='lpepefreitas@gmail.com',
    description='Goal Oriented Action Planning (GOAP) algorithm implemented in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
)
