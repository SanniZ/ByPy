#!/usr/bin/env python3

AUTHOR  = 'Byng Zeng'
VERSION = '1.2.4'

import os

from pybase import pyinput, pysys, pyfile
from crypto.cryptofile import cryptofile
from crypto.cryptokey import cryptokey


DIR = os.path.dirname(os.path.abspath(__file__))
NAME = os.path.basename(__file__)

def markdown_help():
    help_menus = (
        "=====================================",
        "    markdown crypto - %s" % VERSION,
        "=====================================",
        " usage: python3 {} option".format(NAME),
        "",
        " options:",
        "  -k: 16 Bytes key password",
        "  -f: path of key file", 
        "  -s: path of source",
        "  -o: path of output",
        "  -d: decrypto markdown",
        "  -e: encrypto markdown",
    )
    pysys.print_help(help_menus, True)


def markdown_encrypto(key, src, dst):
    if cryptofile.CryptoFile(key, src, dst, 'md', 'mdx').encrypto_files():
        pyfile.remove_type_file(src, 'md')


def markdown_decrypto(key, src, dst):
    if cryptofile.CryptoFile(key, src, dst, 'mdx', 'md').decrypto_files():
        pyfile.remove_type_file(dst, 'mdx')


def markdown(args=None):
    key = None
    key_file_path = None
    src = os.getcwd()
    dst = src
    opts = []
    if not args:
        args = pyinput.get_input_args('dek:f:s:o:h')
        if not args:
            markdown_help()
            exit()
    # set vars.
    for k, v in args.items():
        if v:  # transfer v.
            v = v if type(v) == str else v[0]
        if k == '-k':  # key
            key = v
        elif k == '-f':  # key file.
            key_file_path = os.path.abspath(v)
        elif k == '-s':  # path of source.
            src = os.path.abspath(v)
            dst = src
        elif k == '-o':  # path of output.
            dst = os.path.abspath(v)
        elif k == '-d':  # decrypto.
            opts.append(k)
        elif k == '-e':  # encrypto.
            opts.append(k)
        else:
            markdown_help()
    if not opts:
        return True
    # get key.
    if not key:
        # get key from md5 key file.
        key = cryptokey.get_key_form_file(key_file_path)
        if not key:
            print('No found key!!!')
            return False
    # run opts.
    for opt in opts:
        if opt == '-d':  # decrypto.
            markdown_decrypto(key, src, dst)
        elif opt == '-e':  # encrypto.
            markdown_encrypto(key, src, dst)
    return True

if __name__ == "__main__":
    markdown()
