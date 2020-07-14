#!/usr/bin/env python
# -*-coding:utf-8-*-

from setuptools import setup, find_packages

setup(
    name = 'linuxpy',
    version = '1.0.0',
    keywords = ["linux", "HwInfo", "PsOps", "FileOps", "Shell", 'FileTree'],
    description = 'linux classes, it provides HwInfo, PsOps, FileOps , Alias and Shell modules.',
    author = "Byng.Zeng",
    author_email = "sanni230@126.com",
    url='',
    license = 'GPL',
    py_modules = ['__init__',
                  'alias',
                  'fileops',
                  'hwinfo',
                  'ps',
                  'shell',
                  'rename'],
    packages = ['linuxpy'],
    platforms = 'any',
    requires = [],
    install_requires=['pybase'],

    #entry_points = {
    #    'console_scripts': [
    #        'cpus=pylinux:cpus',
    #        'ipaddr=pylinux:ipaddr',
    #        'aliascmds=pylinux.AliasOpsCmds:main',],
    #},

    #scripts = [
    #    'pylinux/bin/cpus',
    #    'pylinux/bin/ipaddr',
    #],

    zip_safe = True
)
