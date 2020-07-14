#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/07/01

@author: Byng.Zeng
"""

VERSION = '1.0.0'


from . import shell, alias, fileops, hwinfo, ps, rename

lxshell = shell
lxalias = alias
lxfileops = fileops
lxhwinfo = hwinfo
lxps = ps
lxrename = rename

from .alias import (AliasOps, AliasPathOps, AliasOpsCmds)
from .fileops import (FileOps, FileTree, FileTreeCmds)
from .hwinfo import (HwInfo)
from .ps import (PsOps)
from .shell import (execute, Shell)
from .rename import (RenameCmds, rename_path_files, rename_sub, rename_order)