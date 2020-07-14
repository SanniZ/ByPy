#!/usr/bin/env python
# -*- coding:utf=8 -*-


class UsageHelp(object):
    def __init__(self, name=None, version=None, fn=None, usage=None):
        self._name = name if name else self.__class__.__name__
        self._version = version
        self._fn = fn
        self._usage = usage

    def print_usage(self):
        print("==================================================")
        print("  {} - {}".format(self._name, self._version))
        print("==================================================")
        if self._fn:
            print("{}".format(self._fn))
            print("")
        print("usage: python {}.py options".format(self._name))
        print("option:")
        usages = self._usage
        if isinstance(self._usage, (str)):
            usages = self._usage.splitlines()
        for u in usages:
            print("{}".format(u))

    def print_help(self):
        return self.print_usage()


if __name__ == '__main__':
    class Demo(UsageHelp):
        def __init__(self):
            super(Demo, self).__init__(
                version='1.0.0',
                fn='it is sub class of  usagehelp',
                usage = ("  -h      : print help",
                         "  -f path : path for file",
                         "  -s path : path of src")
            )

        def main(self, args=None):
            self.print_help()

    Demo().main()