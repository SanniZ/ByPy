#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.1.0'

import os
import hashlib 
import getpass

from crypto import cryptohelper

KEY_FILE = 'crypto.key'

pr_lvl = ['info', 'err']

def pr_dbg(msg, exit_=False):
    if 'dbg' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def pr_info(msg, exit_=False):
    if 'info' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def pr_err(msg, exit_=False):
    if 'err' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def encrypto_passwd_key(passwd, key):
    if any((not passwd, not key)):
        return None, None
    md5 = hashlib.md5()
    md5.update(passwd.encode())
    passwd_md5 = md5.hexdigest()
    # get iv.
    iv = "{}{}".format(passwd, '*' * (16 - len(passwd)))
    # encrypto now.
    key_md5 = cryptohelper.CryptoHelper(passwd_md5, iv=iv).encrypt(key)
    return passwd_md5, key_md5


def write_passwd_key_to_file(passwd, key, path=None):
    out = KEY_FILE
    passwd_md5, key_md5 = encrypto_passwd_key(passwd, key)
    if any((not passwd_md5, not key_md5)):
        pr_err('error, passwd and key invalid!')
        return False
    if path:
        out = path
    md5 = hashlib.md5()
    md5.update('{}{}'.format(passwd_md5, key_md5).encode())
    passwd_key_md5 = md5.hexdigest()
    with open(out, 'w') as fd:
        fd.write("{}".format(passwd_key_md5))
        fd.write("{}{}".format(passwd_md5, key_md5.decode()))
    return True


def check_passwd_key(data):
    if not data:
        print("Error, no data at passwd key file!")
        return False
    # check passwd and key.
    passwd_key_md5 = data[:32]
    passwd_md5 = data[32:64]
    key_md5 = data[64:]
    # calc passwd and key md5
    md5 = hashlib.md5()
    md5.update('{}{}'.format(passwd_md5, key_md5.encode()).encode())
    passwd_key_md5_2 = md5.hexdigest()
    return True if (passwd_key_md5 == passwd_key_md5_2) else False

def read_passwd_key_from_file(path=None):
    # check path of file.
    if not path:
        # check current folder for mdcrypto.key.
        if os.path.exists(os.path.join(os.getcwd(), KEY_FILE)):            
            path = os.path.join(os.getcwd(), KEY_FILE)
        else:  # get file from system env vars.
            path = os.getenv("KEY_FILE")
    # not found.
    if any((not path, not os.path.exists(path))):  # check path file.
        pr_err('error, %s is invalid!' % path)
        return None, None

    # get passwd and key from file.
    with open(path) as fd:
        passwd_key = fd.read()
    if any((not passwd_key, not check_passwd_key(passwd_key))):
        pr_dbg('error, not get passwd from read file.')
        return None, None
    # get passwd_md5 and key_md5.
    passwd_md5 = passwd_key[32:64]
    key_md5 = passwd_key[64:]
    # return result.
    return passwd_md5, key_md5


def get_key_form_file(path):
    passwd_md5, key_md5 = read_passwd_key_from_file(path)
    if any((not passwd_md5, not key_md5)):
        pr_dbg('get passwd and key of md5 fail.')
        return None
    # check passwd
    passwd = getpass.getpass('Input passwd:')
    md5 = hashlib.md5()
    md5.update(passwd.encode())
    passwd_hex = md5.hexdigest()
    if passwd_hex != passwd_md5:
        pr_err('passwd invalid!')
        return None
    # decrypto key and return.
    iv = "{}{}".format(passwd, '*' * (16 - len(passwd)))
    return cryptohelper.CryptoHelper(passwd_md5, iv=iv).decrypt(key_md5)



class PasswdKeyCmds(object):
    from pybase.pydecorator import get_cmd_args

    def print_usage(self):
        print('==================================')
        print('    md5key - %s' % VERSION)
        print('==================================')
        print('usage: python3 md5key.py options')
        print('')
        print('options:')
        print(' -w passwd : set passwd')
        print(' -k key : set key')
        print(' -f path : create key file to path.')
        print(' -p path : display key of path file.')
        print(' -v      : enable debug mode.')

    @get_cmd_args('w:k:f:p:vh')
    def main(self, args=None):
        passwd = key = None
        opts = dict()
        # check args.
        if not args:
            self.print_usage()
            exit()
        # process args
        for k, v in args.items():
            if v:
                v = v if isinstance(v, str) else v[0]
            # check opts.
            if k == '-w':  # passwd
                passwd = v
            elif k == '-k':  # key
                key = v
            elif k in ['-f', '-p']:
                opts[k] = v
            elif k == '-v':
                pr_lvl.append("dbg")
            else:
                self.print_usage()
                exit()
        # process otps.
        for opt, path in opts.items():
            if opt == '-f':
                if any((not passwd, not key, not path)):
                    pr_err('error, passwd or key error.', True)
                write_passwd_key_to_file(passwd, key, path)
            elif opt == '-p':
                if path:
                    key = get_key_form_file(path)
                    pr_err('get key {}'.format(key if key else 'error'))


# =================================================================
# entrance
# =================================================================
if __name__ == '__main__':
    cmds = PasswdKeyCmds()
    cmds.main()
