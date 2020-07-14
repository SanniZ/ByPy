#!/usr/bin/env python

import os
import sys
import getopt
import glob
#import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8

VERSION = '1.0.2'
AUTHOR  = 'Byng.Zeng'

NAME = os.path.basename(__file__)

verbose = False


# ===========================================
# function APIs
# ===========================================

def get_type_files(path, ftype, recursive=False):
    result = list()
    for rt, ds, fs in os.walk(path):
        if not recursive:
            if rt != path:
                break
        if fs:
            for f in fs:
                if ftype:  ## check ftype
                    if not f.endswith(ftype):
                        continue
                result.append(os.path.join(rt, f))
    return result


def get_extensive_files(path, extensive, recursive=False):
    result = list()
    if path:
        if recursive:
            for rt, ds, fs in os.walk(path):
                result.extend(glob.glob(os.path.join(rt, extensive)))
        else:
            result.extend(glob.glob(os.path.join(path, extensive)))
    else:
        result.extend(glob.glob(extensive))
    return result
        


def rename_order(files, fname, verbose=False):
    # get files of dir.
    dt = dict()
    for f in files:
        path = os.path.dirname(f)
        if path not in dt:
            dt[path] = list()
        dt[path].append(f)
    # rename files of dir.
    total = 0
    for fs in dt.values():
        fdt = dict()
        num = len(fs)
        for index, f in enumerate(fs, 1):
            subfix = os.path.splitext(f)[1]
            # format order of files.
            if num < 10:
                ff = os.path.join(os.path.dirname(f), "{}{:01d}{}".format(fname, index, subfix))
            elif num < 100:
                ff = os.path.join(os.path.dirname(f), "{}{:02d}{}".format(fname, index, subfix))
            elif num < 1000:
                ff = os.path.join(os.path.dirname(f), "{}{:03d}{}".format(fname, index, subfix))
            else:
                ff = os.path.join(os.path.dirname(f), "{}{:d}{}".format(fname, index, subfix))
            fdt[f] = ff
        # check exist files.
        lt = list()
        for f, ff in fdt.items():
            if os.path.exists(ff):
                fdt[f] = fdt[ff]
                lt.append(ff)
        for f in lt:
                fdt.pop(f)
        total += len(fdt)
        # rename files.
        for f, ff in fdt.items():
            # show info
            if verbose:
                print("{:s} -> {:s}".format(f, ff))
            os.rename(f, ff)
    print("\nTotal: {} files".format(total))
    return 0


def rename_sub(files, sub, verbose=False):
    num = len(files)
    # get format to be rename.
    old, new = sub.split(',')
    for index, f in enumerate(files):
        ff = f.replace(old, new)
        if verbose:
            print("{:s} -> {:s}".format(f, ff))
        os.rename(f, ff)
    print("\nTotal: {} files".format(num))
    return 0


def rename_path_files(path, ftype, option, recursive=False, verbose=False):
    # get files.
    fs = None
    if 'ftype' in ftype:
        fs = get_type_files(path, ftype['ftype'], recursive)
    elif 'fextensive' in ftype:
        fs = get_extensive_files(path, ftype['fextensive'], recursive)
    else:
        print("Error, unknown ftype: {}".format(ftype))
        return -1
    # rename files.
    if not fs:
        print("No found files!")
        return -1
    # run option.
    if 'sub' in option:
        return rename_sub(fs, option['sub'], verbose)
    if 'order' in option:
        return rename_order(fs, option['order'], verbose)
    return 0


# ===============================================================
# RenameCmds class
#
# It is the class of process cmds for rename files.
# ===============================================================
class RenameCmds(object):
    def print_usage(self):
        USAGES = [
            '=====================================================',
            '    %s  - %s' % (os.path.splitext(NAME)[0], VERSION),
            '=====================================================',
            'rename files of path',
            '',
            'usage:   python %s option' % NAME,
            '',
            'option:',
            '  [ -p path    | --path=path   ] : path of files',
            '  [ -f .xxx    | --ftype=.xxx  ] : file type .xxx',
            '  [ -e "*.xxx" | --extensive="*.xxx" ] : extensive of *.xxx',
            '  [ -o fmt     | --order=fmt   ] : order fmt files',
            '  [ -s old,new | --sub=old,new ] : sub name of files',
            '  [ -r         | --recursive   ] : recurse directories',
            '  [ -v         | --verbose     ] : show info',
        ]
        for txt in USAGES:
            print(txt)

    def main(self, opts=None):
        if not opts:  # get opts.
            try:
                opts, args = getopt.getopt(sys.argv[1:], 'hp:f:e:s:o:rv', 
                    ['path=', 'ftype=', 'extensive', 'sub=', 'order=', 'recursive', '--verbose'])
            except getopt.GetoptError as e:
                pr_warn(str(e))
                self.print_usage()
                exit()
        # check opts.
        if not opts:
            self.print_usage()
            exit()
        # config args.
        path = os.getcwd()
        ftype = None
        option = None
        recursive = False
        verbose = False
        for opt in opts:
            if opt[0] in ['-p', '--path']:
                path = os.path.abspath(opt[1])
            elif opt[0] in ['-f', '--ftype']:
                ftype = {"ftype": opt[1]}
            elif opt[0] in ['-e', '--fextensive']:
                ftype = {"fextensive": opt[1]}
            elif opt[0] in ['-o', '--order']:
                option =  {"order": opt[1]}
            elif opt[0] in ['-s', '--sub']:
                option = {'sub': opt[1]}
            elif opt[0] in ['-r', '--recursive']:
                recursive = True
            elif opt[0] in ['-v', '--verbose']:
                verbose = True
            elif opt[0] in ['-h', '--help']:
                self.print_usage()
                exit()
        # execute option
        if not option:
            print('no option, -h for help')
            exit()
        # rename files.
        rename_path_files(path, ftype, option,  recursive, verbose)


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    cmds = RenameCmds()
    cmds.main()