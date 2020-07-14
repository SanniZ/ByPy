#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/07/01

@author: Byng.Zeng
"""

VERSION = '1.0.0'

import re

from . import shell


# ================================================
# class : PSTool
# ================================================
#
class PsOps(object):
    @staticmethod
    def get_kw_ps(kw):
        cmd = "ps -ax | grep -iE '%s'" % kw
        res = shell.execute_shell(cmd)
        if res:
            res = res.decode()
        return res

    @staticmethod
    def kill_kw_ps(kw):
        pattern_ps = re.compile('(\d+) (pts|\?)')
        # get ps
        res = PsOps.get_kw_ps()
        # kill pids
        res = pattern_ps.findall(res)
        pids = list(map(lambda x: x[0], res))
        ps = ''
        for p in pids:
            ps += ' %s' % p
        cmd = 'sudo kill -9 %s' % ps
        return shell.execute_shell(cmd)

