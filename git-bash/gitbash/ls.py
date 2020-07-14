#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
#import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8

VERSION = '1.0.1'
AUTHOR  = 'Byng.Zeng'

LOCAL_PATH = os.getcwd()
FTYPE_D = 'd'
FTYPE_F = '-'

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
        '  [-s xxx | --src=xxx  ] : source path',
        '  [-l     | --long     ] : show long format',
        '  [-L     | --line     ] : show line format',
        '  [-T     | --type     ] : show type format',
        '  [-a     | --all      ] : show all of types',
    ]
    for txt in USAGES:
        print(txt)


# ===========================================
# function APIs
# ===========================================
#
def print_list(fs, long_format=False, print_line=False):
    for f in fs[0]:
        if print_line:
            print(f, end=' ')
        else:
            print(f)
    if long_format:
        print('')
        print("%d directories, %d files" % (fs[2], fs[1]))


def get_file_size_str(size):
    if size < 4096:
        return "%3dB" % (size)
    elif size < (4096 * 4096):
        return "%3dK" % (size / (4096))
    elif size < (4096 * 4096 * 4096):
        return "%3dM" % (size / (4096 * 4096))
    elif size < (4096 * 4096 * 4096 * 4096):
        return "%3dG" % (size / (4096 * 4096 * 4096))
    else:
        return "%3dT" % (size / (4096 * 4096 * 4096 * 4096))

def get_file_mode(mode):
    def get_mode(mode):
        o = 'x' if (mode & 0x01) else '-'
        g = 'w' if (mode & 0x02) else '-'
        u = 'r' if (mode & 0x04) else '-'
        return "{}{}{}".format(u, g, o)
    mode = int(oct(mode)[-3:])
    return '{}-{}-{}'.format(get_mode(int((mode / 100) % 10)),
                             get_mode(int((mode / 10) % 10)),
                             get_mode(int(mode % 10)))


def list_path(path, long_format=False, print_type=False, hidden=True):
    exclude_dirs = ['.git']
    fs=os.listdir(path)
    f_cnt = 0
    d_cnt = 0
    ls = list()
    for f in fs:
        ftype = FTYPE_F if os.path.isfile(os.path.join(path, f)) else FTYPE_D
        if ftype == FTYPE_F:
            f_cnt += 1
        elif ftype == FTYPE_D:
            d_cnt += 1
        # get list of path
        if long_format:  # print long format
            info = os.stat(os.path.join(path, f))
            tm = time.localtime(info.st_ctime)
            size = get_file_size_str(info.st_size)
            ls.append("%s%s %5s %4d-%02d-%02d %02d:%02d %-s" % (ftype,
                                                                get_file_mode(info.st_mode),
                                                                size,
                                                                tm.tm_year,
                                                                tm.tm_mon,
                                                                tm.tm_mday,
                                                                tm.tm_hour,
                                                                tm.tm_min,
                                                                f))
        else:
            if hidden:
                if f.startswith('.') or f in exclude_dirs:  # do nothing for .* hidden file.
                    continue
            if print_type:  # print to line
                ls.append("%s %s" % (ftype, f))
            else:
                ls.append(f)
    fs = list()
    fs.append(ls)
    fs.append(f_cnt)
    fs.append(d_cnt)
    return fs



def main(opts=None):
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       'hs:lLTa',
                                       ['src=', 'long', 'line', 'type', 'all'])
        except getopt.GetoptError as e:
            print(str(e), ', -h for help')
            #print_usage()
            exit()

    src = None #LOCAL_PATH
    long_format = False
    print_line = False
    print_type = False
    hidden = True
    for opt in opts:
        if opt[0] in ['-s', '--src']:
            src = os.path.abspath(opt[1])
        elif opt[0] in ['-l', '--long']:
            long_format = True
        elif opt[0] in ['-L', '--line']:
            print_line = True
        elif opt[0] in ['-T', '--type']:
            print_type = True
        elif opt[0] in ['-a', '--all']:
            hidden = False
        else:
            print_usage()
            exit()
    if not src:  # no -s, set default or args.
        if args:
            src = os.path.abspath(args[0])
        else:
            src = LOCAL_PATH
    fs = list_path(src, long_format, print_type, hidden)
    if fs:
        print_list(fs, long_format, print_line)


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    main()