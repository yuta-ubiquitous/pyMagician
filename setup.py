#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

from pyMagician import __author__, __version__, __license__

setup(
        name             = 'pyMagician',
        version          = __version__,
        description      = 'Python module for using irMagician via serial port',
        license          = __license__,
        author           = __author__,
        author_email     = 'yuta-ubiquitous@outlook.jp',
        url              = 'https://github.com/yuta-ubiquitous/pyMagician.git',
        keywords         = 'serial irMagician',
        packages         = find_packages(),
        install_requires = ['pySerial'],
)
