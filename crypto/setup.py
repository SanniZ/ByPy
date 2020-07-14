#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import setup

setup(
    name = 'cryptopy',
    version = '1.0.0',
    keywords = ["crypto", "file", "key"],
    description = 'it provides functions of crypto and key for string and file.',
    author = "Byng.Zeng",
    author_email = "sanni230@126.com",
    url='',
    license = 'GPL',
    py_modules = ['__init__',
                  'cryptoutils',
                  'cryptofile',
                  'cryptokey'],
    packages = ['cryptopy'],
    platforms = 'python3.x',
    requires = ['Crypto', 'rsa'],
    install_requires=['pybase'],

    zip_safe = True
)
