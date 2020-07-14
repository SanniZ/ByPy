#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""
import sys
import getopt

from collections import OrderedDict


VERSION = '1.1.1'


############################################################################
#               functions
############################################################################

def get_input_args_blankspace(opts, args=None, only_args=False, ordered_args=True):
    def get_cmd(val):
        if isinstance(val, str):
            if val.startswith('-'):
                return val
        return None

    def cmd_with_values(cmd):
        opts_length = len(opts)
        for index, opt in enumerate(opts):
            if cmd:
                if cmd[1:] == opt:
                    # check ':' for values.
                    if (index + 1) != opts_length: # is it tail?
                        if opts[index + 1] == ':':
                            return True
        return False

    if ordered_args:
        dt = OrderedDict()
    else:
        dt = dict()
    cmd = None
    cmd_values = None
    cmds = list()

    if args:
        if isinstance(args, list):
            cmds.extend(args)
        elif isinstance(args, dict):
            dt = args

    # get argv input.
    if not only_args:
        cmds.extend(sys.argv[1:])

    for val in cmds:
        start_cmd = get_cmd(val)
        if start_cmd:
            cmd = val
            cmd_values = cmd_with_values(val)
            dt[cmd] = []
        else:
            if cmd_values:
                dt[cmd].append(val)
    return dt

def get_input_args_comma(opts, args=None, only_args=False, ordered_args=True):
    if ordered_args:
        dt = OrderedDict()
    else:
        dt = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        print('%s, -h for help.' % str(e))
        sys.exit()
    else:
        if opts:
            for key, value in opts:
                dt[key] = value
    return dt


def get_input_args(opts, args=None, only_args=False, ordered_args=True, separator='\s'):
    if separator == '\s':
        return get_input_args_blankspace(opts, args, only_args, ordered_args)
    elif separator == ',':
        return get_input_args_comma(opts, args, only_args, ordered_args)
    else:
        return None


def get_args_dict(args, symbol=[':'], ordered_args=True):
    if ordered_args:
        dt = OrderedDict()
    else:
        dt = {}
    key = None
    if type(args) == dict:
        return args
    elif args:
        lt = args.split(',')
        if lt:
            for element in lt:
                for sym in symbol:
                    data = element.split(sym)
                    n = len(data)
                    if n == 2:
                        dt[data[0]] = data[1]
                        key = data[0]
                        break
                if n == 1:
                    dt[key] = dt[key] + ', ' + element
    return dt


############################################################################
#               PySys class
############################################################################

class PyInput (object):

    @staticmethod
    def get_input_args(opts, args=None, only_args=False, ordered_args=True, separator='\s'):
        return get_input_args(opts, args, only_args, ordered_args, separator)

    @staticmethod
    def get_args_dict(args, symbol=[':']):
        return get_args_dict(args, symbol)
