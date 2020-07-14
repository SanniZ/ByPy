#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/07/01

@author: Byng.Zeng
"""

VERSION = '1.0.0'

import os

from collections import OrderedDict

import pybase

NAME = os.path.basename(__file__)

pr = pybase.pyprint.PyPrint()

# ================================================
# class : AliasOps
# ================================================
#
class AliasOps(object):

    def __init__(self, bash_aliases=None):
        self._bash_aliases = bash_aliases

    # list all of alias cmds.
    def list(self, kw=None, kw_cmd=True, bash_aliases=None):
        f_aliases = bash_aliases if bash_aliases else self._bash_aliases
        if not f_aliases:  # check bash.aliases.
            pr.pr_info("error, not set bash_aliases path!")
            return False
        try:  # read aliases.
            with open(f_aliases, 'r') as fd:
                lines = fd.readlines()
        except FileExistsError as e:  ## error, no found file.
            pr.pr_info(str(e))
            return False
        # get alias cmds.
        cmds = dict()
        for line in lines:
            if line.startswith('alias'):
                cmd = line.splitlines()[0].replace('alias ', '').split('=')
                cmds[cmd[0]] = cmd[1]
        # print list
        res = dict()
        for k, v in cmds.items():
            if not kw:  # all of cmds
                res[k] = v
                #pr.pr_info("{0:<10} : {1:<}".format(c, v))
            else:  # kw
                for w in kw.split(','):
                    if kw_cmd:  # only check cmd
                        if w in k:
                            if k not in res.keys():
                                res[k] = v
                    else:  # check cmd and values
                        if w in k or w in v:
                            if k not in res.keys() and v not in res.values():
                                res[k] = v
        # get max length of cmd.
        length = 0
        for k in sorted(res.keys()):
            length = len(k) if len(k) > length else length
        length = len('alias') + 2 if length < len('alias') else length
        # print result.
        pr.pr_info("{0:-^{1:}}   {2:-^32}".format('alias', length, 'command'))
        for k in sorted(res.keys()):
            pr.pr_info("{0:<{1:}} : {2:<}".format(k, length, res[k]))
        # print done: length + command + 3 blank
        pr.pr_info('{}{}{}'.format(('-' * length),
                "all of alias",  ('-' * (32 + 3 - len("all of alias")))))

# ================================================
# class : AliasOps
# ================================================
#
class AliasPathOps(object):

    def __init__(self, bash_alias_path=None):
        self._bash_alias_path = bash_alias_path

    # list all of alias cmds.
    def list(self, kw=None, kw_cmd=True, bash_alias_path=None):
        alias_path = bash_alias_path if bash_alias_path else self._bash_alias_path
        if not alias_path:  # check bash.aliases.
            pr.pr_info("error, not set alias_path path!")
            return False
        try:  # read aliases.
            with open(alias_path, 'r') as fd:
                lines = fd.readlines()
        except FileExistsError as e:  ## error, no found file.
            pr.pr_info(str(e))
            return False
        # get alias cmds.
        cmds = dict()
        for line in lines:
            if line.startswith('export'):
                cmd = line.splitlines()[0].replace('export ', '').split('=')
                cmds[cmd[0]] = cmd[1]
        # print list
        res = dict()
        for k, v in cmds.items():
            if not kw:  # all of cmds
                res[k] = v
                #pr.pr_info("{0:<10} : {1:<}".format(c, v))
            else:  # kw
                for w in kw.split(','):
                    if kw_cmd:  # only check cmd
                        if w in k:
                            if k not in res.keys():
                                res[k] = v
                    else:  # check cmd and values
                        if w in k or w in v:
                            if k not in res.keys() and v not in res.values():
                                res[k] = v
        # get max length of cmd.
        length = 0
        for k in sorted(res.keys()):
            length = len(k) if len(k) > length else length
        length = len('alias') + 2 if length < len('alias') else length
        # print result.
        pr.pr_info("{0:-^{1:}}   {2:-^32}".format('name', length, 'path'))
        for k in sorted(res.keys()):
            pr.pr_info("{0:<{1:}} : {2:<}".format(k, length, res[k]))
        # print done: length + path + 3 blank
        pr.pr_info('{}{}{}'.format(('-' * length),
                "all of export paths",  ('-' * (32 + 3 - len("all of export paths")))))


# ================================================
# class : AliasOpsCmds
# ================================================
#
class AliasOpsCmds(pybase.pyusagehelp.UsageHelp):

    # default bash.aliases file.
    if os.name == 'nt':
        BASH_ALIASES = '{}/bash.aliases.bashrc'.format(os.getenv('_BASHRCPATH'))
    elif os.name == 'posix':
        BASH_ALIASES = "~/.bash.aliases"

    def __init__(self, bash_aliases=BASH_ALIASES):
        self._bash_aliases = bash_aliases
        super(AliasOpsCmds, self).__init__(
             name=os.path.splitext(NAME)[0],
             version=VERSION,
             usage = "  -l kw[,kw]    : list alias cmds.\n" \
                     "  -f path       : path of bash.aliases.\n" \
                     "  -c True/False : only cmd kw.\n" \
                     "\n" \
                     "default:\n" \
                     "  -l None -c True -f {}".format(AliasOpsCmds.BASH_ALIASES),
        )

    def main(self, args=None):
        if not args:
            args =  pybase.pyinput.get_input_args('hl:f:c:p:')
            if not args:
                pr.pr_err("no args, do nothing!")
                return True
        opts = OrderedDict()
        bash_aliases = self._bash_aliases
        check_cmd = True
        for k, v in args.items():
            if v:
                v = v[0] if isinstance(v, list) else v
            if k in ['-l', '-p']:
                opts[k] = v
            elif k in ['-f']:
                bash_aliases = os.path.abspath(v)
            elif k in ['-c']:
                check_cmd = True if v in ['True', True, 'true'] else False
            else:
                self.print_usage()
                return True
        if not bash_aliases:
            pr.pr_err("error, not set -f for bash.aliases file!")
            return False
        # run opts
        for opt, val in opts.items():
            if opt in ['-l']:
                AliasOps(bash_aliases).list(kw=val, kw_cmd=check_cmd)
            elif opt in ['-p']:
                AliasPathOps(bash_aliases).list(kw=val, kw_cmd=check_cmd)
