#!/usr/bin/env python

import os
import sys
import getopt
import serial
import time

#import io
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8


VERSION = '1.0.2'
AUTHOR  = 'Byng.Zeng'

NEW_LINE = '\r\n'

bps = 9600
timeout = 2
times = 1
duration = 0

port = None
options = dict()

OP_READ   = 'OP_READ'
OP_WRITE  = 'OP_WRITE'
OP_RS485X = 'OP_RS485X'

NAME = os.path.basename(__file__)


def pr_info(fmt):
    print(fmt, flush=True)

def serial_flush_input_output(sp, buf_id):
    if buf_id & 0x1:
        sp.flushInput()
    if buf_id & 0x2:
        sp.flushOutput()


def serial_port(port, bps, timex):
    try:
        sp = serial.Serial(port, bps, timeout=timex)
    except serial.serialutil.SerialException as e:
        return None
    return sp


def serial_write_flush(sp):
    return sp.write(NEW_LINE.encode())

def serial_write(sp, data):
    rc = sp.write(data.encode())
    sp.flush()
    #serial_write_flush(sp)
    return rc


def serial_read(sp, size):
    rc = sp.read(size + len(NEW_LINE))
    # sp.flush()
    try:
        rc = rc.decode()
    except UnicodeDecodeError as e:
        return 0
    return rc


# ===============================================================
# UartCmds class
#
# It is the class of process cmds for uart.
# ===============================================================

class UartCmds(object):
    def print_help_usage(self):
        USAGES = (
            '=====================================================',
            '    %s  - %s' % (os.path.splitext(NAME)[0], VERSION),
            '=====================================================',
            'serial option',
            '',
            'usage:   python %s option' % NAME,
            '',
            'option:',
            '  [ -p path | --port=path ] : port of serial',
            '  [ -b n    | --bps=n     ] : file type .xxx',
            '  [ -T n    | --timeout=n ] : num of timeout',
            '  [ -w n    | --write=n   ] : run write n times',
            '  [ -r n    | --read=n    ] : run read n times',
            '  [ -t n    | --times=n   ] : test n times',
            '',
            'default:',
            '  -b {} -T {} -t {} -d {}'.format(bps, timeout, times, duration),
        )
        for txt in USAGES:
            pr_info(txt)

    def main(self, opts=None):
        if not opts:  # get opts.
            try:
                opts, args = getopt.getopt(sys.argv[1:], 'p:b:T:w:r:t:d:Xh',
                                ['port=', 'bps=', 'timeout=', 'duration', 'times', 'rs485x', 'help'])
            except getopt.GetoptError as e:
                pr_info(str(e))
                self.print_help_usage()
                exit()

        # check opts.
        if not opts:
            self.print_help_usage()
            exit()

        global bps
        global timeout
        global times
        global duration
        # config args.
        for opt in opts:
            if opt[0] in ['-p', '--port']:
                port = opt[1]
            elif opt[0] in ['-b', '--bps']:
                bps = opt[1]
            elif opt[0] in ['-T', '--timeout']:
                timeout = float(opt[1])
            elif opt[0] in ['-w', '--write']:
                options[OP_WRITE] = opt[1]
            elif opt[0] in ['-r', '--read']:
                options[OP_READ] = int(opt[1])
            elif opt[0] in ['-t', '--times']:
                times = int(opt[1])
            elif opt[0] in ['-d', '--duration']:
                duration = int(opt[1])
            elif opt[0] in ['-X', '--rs485x']:
                options[OP_RS485X] = None
            elif opt[0] in ['-h', '--help']:
                self.print_help_usage()
                exit()

        if not port:
            pr_info("no port!")
            exit() 
        # execute option
        if not options:
            pr_info('no option, -h for help')
            exit()

        sp = serial_port(port, bps, timeout)
        # pr_info("port:{}, bps:{}, timeout:{}".format(port, bps, timeout))
        if not sp:
            pr_info("Error, Open Serial Port {} fail!".format(port))
            exit()

        for opt, data in options.items():
            if opt == OP_WRITE:
                for i in range(times):
                    serial_flush_input_output(sp, 2)
                    res = serial_write(sp, data)
                    pr_info("write data length: {}".format(res))
                    if duration:
                        time.sleep(duration)
            elif opt == OP_READ:
                for i in range(times):
                    serial_flush_input_output(sp, 1)
                    res = serial_read(sp, data)
                    pr_info("read data: {}".format(res))
                    if duration:
                        time.sleep(duration)
            elif opt == OP_RS485X:
                HELLO_FROM_HOST = "Hi Jerry, I am Tom!"
                HELLO_TO_HOST   = "Hi Tom, I am Jerry!"

                for i in range(times):
                    pr_info("--------------RS485X----------------")
                    pr_info("Host said: {}".format(HELLO_FROM_HOST))
                    #serial_flush_input_output(sp, 3)
                    rc = serial_write(sp, HELLO_FROM_HOST)
                    if rc <= 0:
                        pr_info("Error, it is failed to say hello!");
                        return -1

                    #serial_flush_input_output(sp, 1)
                    rc = serial_read(sp, len(HELLO_TO_HOST))
                    pr_info("Response : {}".format(rc))
                    if isinstance(rc, str):
                        if rc == HELLO_TO_HOST:
                            pr_info("Successful!\n")
                    if duration:
                        time.sleep(duration)
        sp.close()


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    cmds = UartCmds()
    cmds.main()