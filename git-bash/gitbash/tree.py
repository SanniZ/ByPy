#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8


VERSION = '1.0.2'
AUTHOR  = 'Byng.Zeng'

LOCAL_PATH = os.getcwd()
CONFIG_MINTTYRC=0

F_TREE='|-- '
D_TREE='+-- '
TABS='|   '


# ===========================================
# usage
# ===========================================
#
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'usage:   python %s option' % os.path.basename(__file__),
        '',
        'option:',
        '  [-s path | --src=path ] : source path',
        '  [-a      | --all      ] : print all of files',
        '  [-L n    | --depth=n  ] : print depth of tree',

    ]
    for txt in USAGES:
        print(txt)



# ===========================================
# function APIs
# ===========================================
#
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

def main(opts=None):
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hs:aL:', ['src=', 'all', 'depth'])
        except getopt.GetoptError as e:
            print(str(e), ', -h for help')
            #print_usage()
            exit()

    src = None # LOCAL_PATH
    hidden = True
    depth_max = 0
    for opt in opts:
        if opt[0] in ['-s', '--src']:
            src = os.path.abspath(opt[1])
        elif opt[0] in ['-a', '--all']:
            hidden = False
        elif opt[0] in ['-L', '--depth']:
            depth_max = int(opt[1])
        else:
            print_usage()
            exit()
    if not src:  # no -s, set default or args.
        if args:
            src = os.path.abspath(args[0])
        else:
            src = LOCAL_PATH
    # print tree
    print_tree(src, hidden, depth_max)


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    main()