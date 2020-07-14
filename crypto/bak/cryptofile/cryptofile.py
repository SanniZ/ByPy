#!/usr/bin/env python3

AUTHOR='Byng Zeng'
VERSION='1.1.0'

import os

from pybase import pyinput, pysys, pyfile
from crypto import cryptohelper
from crypto.cryptokey import cryptokey

NAME = os.path.basename(__file__)

#######################################################
# Function APIs
#######################################################

_pr = False

#
# set print msg
#
def set_pr(pr):
    global _pr
    _pr = pr

#
# print msg
#
def pr_info(msg):
    global _pr
    if _pr:
        print(msg)


#
# return list of type files.
# 
# path: dir of path to find.
# ftype: type of file, example: txt, md.
#
# return None or list.
#
def get_type_files(path, ftype):
    if any((not path, not ftype)):
        return None
    else:
        fs = dict()
        if os.path.isfile(path):
            fs[os.path.basename(path)] = os.path.dirname(path)
        else:
            fs = pyfile.find(path, ftype=ftype)
        return fs



#
# encrypt files of path.
#
# key: key to encrypto.
# src: path of source.
# dst: path of output.
#
# return None or list.
#
def encrypto_path_files(key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        enc = cryptohelper.CryptoHelper(key, cipher=cipher, mode=mode)
        res = []
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r', encoding='UTF-8') as fd:
                f = fd.read()
            f = enc.encrypt(f)
            if not f:
                # print('stop, encrypto %s failed!' % os.path.join(v,k))
                # return False
                continue
            dr = v.replace(src, '')
            if not os.path.exists(os.path.join(dst, dr)):
                os.makedirs(os.path.join(dst, dr))
            if xtype:
                k = k.replace(ftype, xtype)
            else:
                k = k.replace(ftype, "%sx" % ftype)
            fx = os.path.join(dst, dr, k)
            res.append(fx)
            pr_info("out: %s" % fx)
            with open(fx, 'w', encoding='UTF-8') as fd:
                fd.write(f.decode())
        # return res list.
        return res
    else:
        return None



#
# decrypt files of path.
#
# key: key to decrypto.
# src: path of source.
# dst: path of output.
#
# return None or list.
#
def decrypto_path_files(key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        dec = cryptohelper.CryptoHelper(key=key, cipher=cipher, mode=mode)
        res = []
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r', encoding='UTF-8') as fd:
                f = fd.read()
            f = dec.decrypt(f.encode())
            if not f:
                print('stop, decrypto %s failed' % os.path.join(v, k))
                return False
            dr = v.replace(src, '')
            if not os.path.exists(os.path.join(dst, dr)):
                os.makedirs(os.path.join(dst, dr))
            if xtype:
                k = k.replace(ftype, xtype)
            else:
                k = k.replace(ftype, ftype[:-1])
            fdx = os.path.join(dst, dr, k)
            res.append(fdx)
            pr_info("out: %s" % fdx)
            with open(fdx, 'w', encoding='UTF-8') as fd:
                fd.write(f)
        # reutrn res list.
        return res
    else:
        return None


#######################################################
# class:  CryptoFile
#######################################################

class CryptoFile(object):
    def __init__(self, key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
        self._key = key
        if os.path.isfile(src):
            self._src = src
        else:
            self._src = os.path.abspath(src) + '/'
        if os.path.isfile(dst):
            self._dst = os.path.dirname(dst) + '/'
        else:
            self._dst = os.path.abspath(dst) + '/'
        self._ftype = ftype
        self._xtype = xtype
        self._cipher = cipher
        self._mode = mode

    def encrypto_files(self):
        return encrypto_path_files(self._key, self._src, self._dst, self._ftype, self._xtype, self._cipher, self._mode)

    def decrypto_files(self):
        return decrypto_path_files(self._key, self._src, self._dst, self._ftype, self._xtype, self._cipher, self._mode)

    def set_pr(self, pr):
        if pr:
            set_pr(True)
        else:
            set_pr(False)


# -------------------------------------------------
# remove file of src and ftype.
# ------------------------------------------------
def remove_ftype_files(src, ftype):
    if os.path.isfile(src):
        os.remove(src)
    else:
        pyfile.remove_type_file(src, ftype)


# -------------------------------------------------
# encrypto ftype files.
# ------------------------------------------------)
def encrypto_ftype_files(key, src, dst, ftypes):
    for ft in ftypes:
        if CryptoFile(key, src, dst, ft).encrypto_files():
            remove_ftype_files(src, ft)


# -------------------------------------------------
# decrypto ftype files.
# ------------------------------------------------
def  decrypto_ftype_files(key, src, dst, ftypes):
    for ft in ftypes:
        if CryptoFile(key, src, dst, ft).decrypto_files():
            # remove_ftype_files(src, ft)
            pass


# ===============================================================
# CryptoTypeFiles class
#
# It is the class of crypto type files.
# ==============================================================

class CryptoFileType(object):
    def __init__(self, key=None, src=None, dst=None, ftypes=None):
        self._key = key
        self._src = src
        self._dst = dst
        self._ftypes = ftypes

    def encrypto_files(self, key=None, src=None, dst=None, ftypes=None):
        key = key if key else self._key
        src = src if src else self._src
        dst = dst if dst else self._dst
        ftypes = ftypes if ftypes else self._ftypes
        return encrypto_ftype_files(key, src, dst, ftypes)

    def decrypto_files(self, key=None, src=None, dst=None, ftypes=None):
        key = key if key else self._key
        src = src if src else self._src
        dst = dst if dst else self._dst
        ftypes = ftypes if ftypes else self._ftypes
        return decrypto_ftype_files(key, src, dst, ftypes)

    def remove_files(self, src, ftype):
        return remove_ftype_files(src, ftype)


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
            if not args:
                self.print_help_enum()
                return False
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
            self.print_help_enum()
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
        for opt in opts:
            if opt == '-d':  # decrypto.
                CryptoFileType(key, src, dst, ftypes).decrypto_files()
            elif opt == '-e':  # encrypto.
                CryptoFileType(key, src, dst, ftypes).encrypto_files()
        # exit
        return True


# ===========================================
# entrance
# ===========================================
#
if __name__ == "__main__":
    cmds = CryptoFileTypeCmds()
    cmds.main()