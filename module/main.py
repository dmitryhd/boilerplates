#!/usr/bin/env python3

"""
Executable file.
"""

import argparse


from . import logger
from . import config
from . import __version__, __release_date__

work_dir = config.Config['General']['WorkingDir']
log = logger.configure_logger(config.LOGGER_NAME, log_dir=work_dir)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', choices=['generate', 'send'])
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + __version__ + ' released: ' + __release_date__)
    args = parser.parse_args()
    return args


def main():
    if config.Config['General']['SkipMode']:
        log.info('Skipping this start')
        return
    args = parse_args()
    log.info('set working dir to: {}'.format(work_dir))
    if args.command == 'generate':
        pass
    elif args.command == 'send':
        pass
    else:
        pass


if __name__ == '__main__':  # pragma: no cover
    main()
