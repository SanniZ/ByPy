#!/usr/bin/env python

import os

import pybase
import pylinux

class PySetup(pybase.UsageHelp):
    def __init__(self, path=None):
        self._path = path
        super(PySetup, self).__init__(
            version = '1.0.0',
            usage = "  -p path    : path of code\n" \
                    "  -b egg/whl : build to .egg/.whl\n" \
                    "  -i path    : install for path."
        )

    @staticmethod
    def build_egg(path=None):
        print(os.getcwd())
        os.chdir(path)
        print(os.getcwd())
        if os.path.exists("setup.py"):
            cmd = 'python setup.py bdist_egg'
            pylinux.Shell.execute(cmd, True)

    @staticmethod
    def build_whl(path=None):
        print(os.getcwd())
        os.chdir(path)
        print(os.getcwd())
        if os.path.exists("setup.py"):
            cmd = 'python setup.py bdist_wheel'
            pylinux.Shell.execute(cmd, True)

    @staticmethod
    def pip_install(path):
        for rt, ds, fs in os.walk(path):
            if fs:
                for f in fs:
                    if os.path.splitext(f)[1] in ['.egg', '.whl']:
                        cmd = 'pip install {}'.format(os.path.join(rt,f))
                        pylinux.Shell.execute(cmd, True)

    def main(self):
        args = pyinput.get_input_args('hp:b:i:')
        if not args:
            return True
        path = os.getcwd()
        bdist = None
        oinst = None
        for k, v in args.items():
            if v:
                v = v[0] if isinstance(v, list) else v
            if k in ['-p']:
                path = v
            elif k in ['-b']:
                if v in ['egg']:
                    bdist = 'bdist_egg'
                elif v in ['whl', 'wheel']:
                    bdist = 'bdist_whl'
            elif k in ['-i']:
                oinst = v
            else:
                self.print_help()
                return True

        if bdist == 'bdist_egg':
            PySetup.build_egg(path)
        if bdist == 'bdist_whl':
            PySetup.build_whl(path)
        if oinst:
            PySetup.pip_install(oinst)


if __name__ == '__main__':
    PySetup().main()