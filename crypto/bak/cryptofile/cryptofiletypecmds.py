#!/usr/bin/env python

AUTHOR  = 'Byng Zeng'
VERSION = '1.0.2'

import os

from pybase import pyinput, pysys
from crypto.cryptofile import cryptofile
from crypto.cryptokey import cryptokey


# DIR  = os.path.dirname(os.path.abspath(__file__))
NAME = os.path.basename(__file__)


# ===============================================================
# CryptoTypeFilesCmds class
#
# It is the class of process cmds for crypto type files.
# ===============================================================

class CryptoFileTypeCmds(object):
    # print help
    def  print_help_enum(self):
        help_menus = (
            "=====================================",
            "   {} - {}".format(os.path.splitext(NAME)[0], VERSION),
            "=====================================",
            " usage: python {} option".format(NAME),
            "",
            " options:",
            "    -k passwd : 16 Bytes key password",
            "    -f flie   : path of key file", 
            "    -s path   : path of source",
            "    -o path   : path of output, default to -s",
            "    -d ftype  : decrypto ftype(md,txt,...) files",
            "    -e ftype  : encrypto ftype(mdx,txtx,...) file,",
            "",
            "*** Only support to python 3.x ***",
            "",
            " example:",
            "    -K enc.key -s path -d md,txt",
        )
        pysys.print_help(help_menus, True)

    # main for cmds.
    def main(self, args=None):
        key = None
        key_file_path = None
        src = os.getcwd()
        dst = src
        opts = list()
        ftypes = list()
        # check args.
        if not args:
            args = pyinput.get_input_args('k:f:s::o:e:d:h')
        # set vars.
        for k, v in args.items():
            if v:  # transfer v.
                v = v if isinstance(v, str) else v[0]
            if k == '-k':  # key
                key = v
            elif k == '-f':  # key file.
                key_file_path = os.path.abspath(v)
            elif k == '-s':  # path of source.
                if v:
                    src = os.path.abspath(v)
                    dst = src
            elif k == '-o':  # path of output.
                if v:
                    dst = os.path.abspath(v)
            elif k == '-d':  # decrypto.
                opts.append(k)
                if not v:
                    print("{} No ftype, -h for help".format(k))
                    return False
                ftypes = v.split(',')
            elif k == '-e':  # encrypto.
                opts.append(k)
                if not v:
                    print("{} No ftype, -h for help".format(k))
                    return False
                ftypes = v.split(',')
            elif k == '-h':  # help
                self.print_help_enum()
                exit()
            else:
                print("unknown {}, -h for help".format(k))
                # self.print_help_enum()
                exit()
        # check opts
        if not opts:
            print("No opts, -h for help!")
            return False
        # check ftypes
        if not ftypes:
            print("No ftype, -h for help!")
            return False
        # get key.
        if not key:
            # get key from md5 key file.
            key = cryptokey.get_key_form_file(key_file_path)
            if not key:
                print('No found key!!!')
                return False
        # run opts.
        cryptofile.CryptoTypeFiles()
        for opt in opts:
            if opt == '-d':  # decrypto.
                cryptofile.CryptoFileType().decrypto_files(key, src, dst, ftypes)
            elif opt == '-e':  # encrypto.
                cryptofile.CryptoFileType().encrypto_files(key, src, dst, ftypes)
        # exit
        return True


# ===========================================
# entrance
# ===========================================
#
if __name__ == "__main__":
    cmds = CryptoFileTypeCmds()
    cmds.main()