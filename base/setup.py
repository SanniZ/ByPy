#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import setup

setup(
    name = 'pybase',
    version = '1.0.0',
    keywords = [],
    description = "ByPy basic lib",
    author = "Byng.Zeng",
    author_email = "sanni230@126.com",
    url='',
    license = 'GPL',
    py_modules = ['__init__',
                  'decorator',
                  "input",
                  "file",
                  "image",
                  'path',
                  'print',
                  'sys',
                  'usagehelp'],
    packages = ['pybase'],
    platforms = 'any',
    requires = [],
    install_requires=[],

    zip_safe = True
)
