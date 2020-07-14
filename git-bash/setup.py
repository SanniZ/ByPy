#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import setup, find_packages

setup(
    name = 'gitbash',
    version = '1.0.0',
    keywords = ["tree", 'ls'],
    description = "it provides tree, ls modules for git-base in windows.",
    author = "Byng.Zeng",
    author_email = "sanni230@126.com",
    url='',
    license = 'GPL',
    py_modules = ['__init__', "tree", 'ls'],
    packages = ['gitbash'],
    platforms = 'any',

    zip_safe = True
)
