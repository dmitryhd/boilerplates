#!/usr/bin/env python3

import sys
import os.path as path
# owww ;-(
current_dir = path.dirname(path.realpath(__file__))
sys.path.append(current_dir)

from crm_mini import main

if __name__ == '__main__':
    main.main()
