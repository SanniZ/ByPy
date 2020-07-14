#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/07/01

@author: Byng.Zeng
"""

VERSION = '1.0.0'

import subprocess


def execute(cmd, show=False):
    if show:
        print(cmd)
    try:
        result = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        return None
    else:
            return result

# ================================================
# class : Shell
# ================================================
#
class Shell(object):
    @staticmethod
    def execute(cmd, show=False):
        return execute(cmd, show)


