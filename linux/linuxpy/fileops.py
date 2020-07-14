#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/06/30

@author: Byng.Zeng
"""

VERSION = '1.0.0'

import os
import sys
#import io

import pybase
from . import shell

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8


# ================================================
# class : FileOps
# ================================================
#
class FileOps(object):
    @staticmethod
    def delete(f):
        cmd = r'rm -rf %s' % f
        return shell.execute(cmd)

    @staticmethod
    def find(path, name):
        cmd = r'find %s -name %s' % (path, name)
        return shell.execute(cmd)

    @staticmethod
    def find_delete(path, name):
        cmd = r'find %s -name %s | xargs rm -rf {}' % (path, name)
        return shell.execute(cmd)


# ===========================================
# File Tree APIs
# ===========================================
#
LOCAL_PATH = os.getcwd()

F_TREE='|-- '
D_TREE='+-- '
TABS='|   '

def get_depth_of_path(path):
    return path.count('\\')


def get_tabs_of_path(path):
    depth = get_depth_of_path(path)
    if depth:
        return TABS * (depth - 1), depth
    else:
        return '', 0


def print_tree(src, hidden=True, depth_max=0):
    exclude_dirs = ['.git']
    f_cnt = 0
    d_cnt = 0
    for rt, ds, fs in os.walk(src):
        # get dirname
        rt = rt.replace('%s' % src, '').replace('^\\', '')
        if hidden:
            if rt.startswith('.'):  # do nothing for .* hidden file.
                continue
            else:
                exclude = False
                for d in exclude_dirs:  # check exclude_dirs
                    if d in rt:
                        exclude = True
                        break
                if exclude: # do next for exclude
                    continue
        # get tabs of rt
        tabs, depth = get_tabs_of_path(rt)
        if depth_max and int(depth) > int(depth_max):
            continue
        # print dir
        d_cnt += 1
        d = str((tabs + D_TREE + os.path.basename(rt)) if (len(rt[1:])) else '.')
        print(d)
        if depth_max and int(depth) == int(depth_max):
            continue
        # print file
        for index, f in enumerate(fs):
            if hidden:
                if f.startswith('.'):  # do nothing for .* hidden file.
                    continue
            f_cnt += 1
            f = str(tabs + TABS + F_TREE + f) if depth else str(F_TREE + f)
            print(f)
    print("")
    print("%d directories, %d files" % (d_cnt - 1, f_cnt))  # do not include root dir.


# ================================================
# class : FileTree
# ================================================
#
class FileTree(object):

    @staticmethod
    def print_tree(src, hidden=True, depth_max=0):
        return print_tree(src, hidden, depth_max)


# ================================================
# class : FileTreeCmds
# ================================================
#
class FileTreeCmds(pybase.pyusagehelp.UsageHelp):

    def __init__(self):
        super(FileTreeCmds, self).__init__(
            fn = 'print file tree',
            usage = '[-s path | --src=path ] : source path\n' \
                    '[-a      | --all      ] : print all of files\n' \
                    '[-L n    | --depth=n  ] : print depth of tree\n'
        )

    def main(self, args=None):
        # get opts.
        if not args:
            args = pybase.pyinput.get_input_args('hs::aL:')
        #  process opts.
        src = LOCAL_PATH # LOCAL_PATH
        hidden = True
        depth_max = 0
        if args:
            for k, v in args.items():
                if v:
                    v = v[0] if isinstance(v, list) else v
                # opt
                if k in ['-s', '--src']:
                    if v:
                        src = os.path.abspath(v)
                elif k in ['-a', '--all']:
                    hidden = False
                elif k in ['-L', '--depth']:
                    depth_max = int(v)
                else:
                    self.print_help()
                    return False
        # print tree
        FileTree.print_tree(src, hidden, depth_max)