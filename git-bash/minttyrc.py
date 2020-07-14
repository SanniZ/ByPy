#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

MINTTYRC=os.path.join("C:\\", 'Users', 'zengyingbin', '.minttyrc')

def get_minttyrc_lang():
    with open(MINTTYRC, 'r') as fd:
        lines = fd.readlines()
        for index, line in enumerate(lines):
            if 'Charset' in line:
                return line.replace('Charset=', '').replace('\n', '')
    return None

def set_minttyrc_lang(lang):
    with open(MINTTYRC, 'r') as fd:
        lines = fd.readlines()
        for index, line in enumerate(lines):
            if 'Charset' in line:
                lines[index] = 'Charset=%s\n' % lang
                break
    with open(MINTTYRC, 'w') as fd:
        fd.writelines(lines)
