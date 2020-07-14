#!/usr/bin/env python

import json
import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8


def print_personal(dt):
    for k, v in dt.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                print("{}:{}".format(kk, vv))
        else:
            print("{}:{}".format(k, v))
        print("\n---------------------------\n")


if __name__ == '__main__':
    with open('Personal.json', encoding="utf-8") as fd:
        js = fd.read()
        dt = json.loads(js)
    print_personal(dt)