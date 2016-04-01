#!/usr/bin/env python3

import os.path as path

class Context:
    def __init__(self, config: dict):
        self.working_dir = config['General']['WorkingDir']
        self.log_file = path.join(self.working_dir, 'aaa.log')

    @staticmethod
    def _touch_file(filename):
        with open(filename, 'w') as fd:
            fd.write(' ')

    @staticmethod
    def _read_file(filename):
        if not path.isfile(filename):
            Context._touch_file(filename)
        with open(filename, 'r') as fd:
            return fd.read()

    @staticmethod
    def _write_file(filename, content):
        with open(filename, 'w') as fd:
            return fd.write(content)

    def get_recipients(self):
        return self._read_file(self.recipients)

    def set_recipients(self, content):
        return self._write_file(self.recipients, content)

