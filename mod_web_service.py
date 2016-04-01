#!/usr/bin/env python3

import os
import sys
import subprocess as sp

PROCESS_NAME = 'crm_mini_web.py'
WORKING_DIR = 'crm-mini/'
START_COMMAND = '/usr/bin/nohup python3 {}crm_mini_web.py &'.format(WORKING_DIR)
STOP_COMMAND = 'pkill -f ".*{}.*"'.format(PROCESS_NAME)
STATUS_COMMAND = 'pgrep -f ".*{}.*"'.format(PROCESS_NAME)


def start():
    os.system(START_COMMAND)


def stop():
    os.system(STOP_COMMAND)


def status() -> bool:
    res = sp.check_output(STATUS_COMMAND, shell=True, universal_newlines=False)
    res = res.decode('utf-8')
    res = res.split('\n')
    res = [s for s in res if s]
    proc_num = len(res) - 1
    if proc_num > 0:
        print('running')
    else:
        print('stopped')
    return proc_num > 0


def main():
    commands = {
        'start': start,
        'stop': stop,
        'status': status,
    }
    if len(sys.argv) != 2:
        print('give arguments')
        return
    command = sys.argv[1]
    commands[command]()


if __name__ == '__main__':
    main()
