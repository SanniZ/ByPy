#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import find_packages
from distutils.core import setup

setup(
    name = 'pytools',
    version = '1.0.0',
    keywords = ["audio", "baiduyun", "ios", "markdown", "py2so", "wiz", "pyc", "uart"],
    description = "crypto helper to file",
    author = "Byng.Zeng",
    author_email = "byng139@139.com",
    url='',
    license = 'GPLv2',
    py_modules = ['setup', 'cleanpyc', 'pathcounter', 'uart'],
    packages = find_packages(),
    platforms = 'any',

    zip_safe = True
)
