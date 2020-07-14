#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/07/01

@author: Byng.Zeng
"""

VERSION = '1.0.0'

import socket

from . import shell


# ================================================
# Function APIs
# ================================================
#
def _get_cpus():
    cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
    return int(shell.execute(cmd))


def _get_ipaddr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        addr = s.getsockname()[0]
    finally:
        s.close()
    return addr


# ================================================
# class : HwInfo
# ================================================
#
class HwInfo(object):
    @staticmethod
    def cpus():
        return _get_cpus()

    @staticmethod
    def ipaddr():
        return _get_ipaddr()

cpus = HwInfo.cpus
ipaddr = HwInfo.ipaddr