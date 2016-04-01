import sys
import os.path as path
from contextlib import suppress
import os


# owww ;-(
current_dir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(current_dir, '..'))


with suppress(FileExistsError):
    os.mkdir('/tmp/crm-mini/')

