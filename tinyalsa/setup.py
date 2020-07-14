#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import setup, find_packages

setup(
    name = 'tinyalsa',
    version = '1.0.0',
    keywords = ["tinymix", "tinycap", "tinywidget"],
    description = "tinyalsa tools, it provides tinymix, tinycap, tinywidget modules.",
    author = "Byng.Zeng",
    author_email = "sanni230@126.com",
    url='',
    license = 'GPL',
    py_modules = ['__init__',
                  "tinymix",
                  "tinycap",
                  "tinywidget"],
    packages = ['tinyalsa'],
    package_dir = {},
    platforms = 'any',
    requires = [],
    install_requires=[],

    zip_safe = True
)
