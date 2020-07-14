#!/usr/bin/env python3
# -*- coding: utf=8 -*-

AUTHOR = 'Byng Zeng'
VERSION = '1.2.0'

import os
import hashlib 
import getpass
import random
import datetime

from pybase import pyinput
from . import cryptoutils

KEY_FILE = 'crypto.key'

KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+<>'

def get_md5_hex(data):
    md5 = hashlib.md5()
    md5.update('{}'.format(data).encode())
    return md5.hexdigest()

def encrypto_key(passwd, key, encrypto, cipher='AES', mode='CBC', iv=None):
    if any((not passwd, not key)):
        print("encrypto_key: error, not passwd_md or key!")
        return None, None
    # config passwd.
    passwd = "{}{}".format(passwd, ' ' * (16 - len(passwd)))
    iv = "{}{}".format(iv, ' ' * (16 - len(iv))) if iv else None
    # get enc key.
    return cryptoutils.CryptoUtils(passwd, iv=iv).encrypt(key)

def decrypto_key(passwd, key_enc, cipher='AES', mode='CBC', iv=None):
    if any((not passwd, not key_enc)):
        return None, None
    # config passwd.
    passwd = "{}{}".format(passwd, ' ' * (16 - len(passwd)))
    iv = "{}{}".format(iv, ' ' * (16 - len(iv))) if iv else None
    return cryptoutils.CryptoUtils(passwd, iv=iv).decrypt(key_enc)


def key_is_invalid(key, key_md5):
    key_md5_hex = get_md5_hex('{}'.format(key).encode())
    return True if key_md5_hex == key_md5 else False


def encrypto_key_file_info(cipher='AES', mode='CBC', iv=''):
    randoms = ''.join(random.sample(KEY_CHARS, 16))
    version = "{}{}".format('Ver#' + VERSION, ' ' * (16 - len('Ver#' + VERSION)))
    signature = 'Byng.Zeng'
    signature = signature[:16] if len(signature) > 16 else '' + signature + ' ' * (16 - len(signature))
    build_time = str(datetime.datetime.now())
    build_time = build_time[:32] if len(build_time) > 32 else '' + build_time + ' ' * (32 - len(build_time))
    others = ' '
    others = others[:16] if len(others) > 16 else '' + others + ' ' * (16 - len(others))
    cipher_mode = cipher + ' ' * (4 - len(cipher)) + mode + ' ' * (4 - len(mode))
    iv = iv[:16] if len(iv) > 16 else '' + iv + ' ' * (16 - len(iv))
    info = '' + version + signature + build_time + others + cipher_mode + iv
    # print('info length: ', len(info))
    return randoms, cryptoutils.CryptoUtils(randoms).encrypt(info)


def decrypto_key_file_info(data):
    version = cipher = mode = iv = None
    randoms = data[:16]
    enc_info = data[16:168]
    dec_data = cryptoutils.CryptoUtils(randoms).decrypt(enc_info)
    if dec_data:
        version = dec_data[:16]
        signature = dec_data[16:32]
        build = dec_data[32:64]
        others = dec_data[64:80]
        others = others[0] if others else None
        cipher = dec_data[80:84]
        mode = dec_data[84:88]
        iv = dec_data[88:]
        iv = iv[0] if iv else None
    return version, signature, build, others, cipher, mode, iv


def write_passwd_key_to_file(passwd, key, path=None, cipher='AES', mode='CBC', iv=None):
    out = path if path else KEY_FILE
    # get randoms and enc_info
    randoms, info_enc = encrypto_key_file_info()
    # print('info_enc length: ', len(info_enc))
    # get passwd_md5 and key_enc
    passwd_md5 = get_md5_hex(passwd.encode())
    key_md5 = get_md5_hex(key.encode())
    iv = iv if iv else randoms
    key_enc = encrypto_key(passwd, key, cipher, mode, iv)
    if any((not passwd_md5, not key_md5, not key_enc)):
        print('error, passwd or key invalid!')
        return False
    # save keys.
    with open(out, 'w') as fd:
        fd.write("{}{}".format(randoms, info_enc.decode()))
        fd.write("{}{}{}".format(passwd_md5, key_md5, key_enc.decode()))
    print(f"output: {out}")
    return True


def read_passwd_key_md5(path=None):
    # check path of file.
    if not path:
        # check current folder for mdcrypto.key.
        if os.path.exists(os.path.join(os.getcwd(), KEY_FILE)):            
            path = os.path.join(os.getcwd(), KEY_FILE)
        else:  # get file from system env vars.
            path = os.getenv("KEY_FILE")
    # not found.
    if any((not path, not os.path.exists(path))):  # check path file.
        print('error, %s is invalid!' % path)
        return None, None
    # get passwd and key from file.
    with open(path) as fd:
        data = fd.read()
    #check version info.
    try:
        version, signature, build, others, cipher, mode, iv = decrypto_key_file_info(data)
    except UnicodeDecodeError as e:
        print('error: ', str(e))
        return None, None, None
    else:
        vsplit = version.split('#')
        if len(vsplit) > 1: # found 'Ver#x.x.x'
            version = vsplit[1].split('.')
            _version = VERSION.split('.')
            if all((version[0] == _version[0], version[1] == _version[1])):
                passwd_key = data[168:] # randoms[16B] + info_enc[128B]
            else:
                print("error, version is invalid!")
                return None, None, None
        else:  # no version info.
            print("error, found invalid data!")
            return None, None, None
    # get passwd_md5 and key_md5.
    passwd_md5 = passwd_key[0:32]
    key_md5 = passwd_key[32:64]
    key_enc = passwd_key[64:]
    # return result.
    return passwd_md5, key_md5, key_enc


def read_key_form_file(path, passwd=None, cipher='AES', mode='CBC', iv=None):
    passwd_md5, key_md5, key_enc = read_passwd_key_md5(path)
    if any((not passwd_md5, not key_md5, not key_enc)):
        print('get md5 passwd or key fail.')
        return None
    # check passwd
    if not passwd:
        passwd = getpass.getpass('Input passwd:')
    passwd_hex = get_md5_hex(passwd.encode())
    if passwd_hex != passwd_md5:
        print('passwd invalid!')
        return None
    # decrypto key and return.
    key = decrypto_key(passwd, key_enc, cipher, mode, iv)
    return key if key_is_invalid(key, key_md5) else None


class CryptoKey(object):
    def __init__(self, passwd=None, key=None, key_path=None, cipher='AES', mode='CBC', iv=None):
        self._passwd = passwd
        self._key = key
        self._key_path = key_path
        self._cipher = cipher
        self._mode = mode
        self._iv = iv

    def get_key_from_file(self, path=None, passwd=None, cipher='AES', mode='CBC', iv=None):
        kpath = path if path else self._key_path
        passwd = passwd if passwd else self._passwd
        cipher = cipher if cipher else self._cipher
        mode = mode if mode else self._mode
        iv = iv if iv else self._iv
        return read_key_form_file(kpath, passwd, cipher, mode, iv)

    def set_passwd_key_to_file(self,
            passwd=None, key=None, path=None, cipher='AES', mode='CBC', iv=None):
        passwd = passwd if passwd else self._passwd
        key = key if key else self._key
        path = path if path else self._key_path
        cipher = cipher if cipher else self._cipher
        mode = mode if mode else self._mode
        iv = iv if iv else self._iv
        return write_passwd_key_to_file(passwd, key, path, cipher, mode, iv)

    # return version, cipher, mode, iv
    def get_key_file_info(self, path=None):
        kpath = path if path else self._key_path
        with open(path) as fd:
            data = fd.read()
        return decrypto_key_file_info(data)


class CryptoKeyCmds(object):

    def print_usage(self):
        print('==================================')
        print('    md5key - %s' % VERSION)
        print('==================================')
        print('usage: python3 md5key.py options')
        print('')
        print('options:')
        print(' -w passwd : set passwd')
        print(' -k key : set key')
        print(' -c path : create key file to path.')
        print(' -r path : read key of path file.')
        print(' -v      : enable debug mode.')

    def main(self, args=None):
        passwd = key = None
        opts = dict()
        # check args.
        if not args:
            args = pyinput.get_input_args('w:k:c:r:h')
            if not args:
                self.print_usage()
                exit()
        if '-h' in args:
            self.print_usage()
            return True
        # process args
        for k, v in args.items():
            if v:
                v = v if isinstance(v, str) else v[0]
            # check opts.
            if k == '-w':  # passwd
                passwd = v
            elif k == '-k':  # key
                key = v
            elif k in ['-c', '-r']:
                opts[k] = v
            else:
                self.print_usage()
                exit()
        # process otps.
        for opt, path in opts.items():
            if opt == '-c':
                if any((not passwd, not key, not path)):
                    print('error, passwd or key error.', True)
                CryptoKey(passwd, key).set_passwd_key_to_file(path=path)
            elif opt == '-r':
                if path:
                    ckey = CryptoKey(passwd=passwd, key_path=path)
                    version, signature, build, others, cipher, mode, iv = ckey.get_key_file_info(path)
                    print("version   : {}".format(version))
                    print("signature : {}".format(signature))
                    print("build     : {}".format(build))
                    print("others    : {}".format(others))
                    print("cipher    : {}".format(cipher))
                    print("mode      : {}".format(mode))
                    key = ckey.get_key_from_file()
                    print('key       : {}'.format(key if key else 'error'))


# =================================================================
# entrance
# =================================================================
if __name__ == '__main__':
    cmds = CryptoKeyCmds()
    cmds.main()
