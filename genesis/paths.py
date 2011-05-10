
from os.path import dirname, expanduser, join, sep

HOME = expanduser('~')
USER_CONFIG = join(HOME, '.genesis')

SOURCE = dirname(__file__)
PACKAGE_CONFIG = join(SOURCE, 'config')


def tilde_encode(filename):
    home = expanduser('~')
    if filename.startswith(home):
        return '~' + sep + filename[len(home)+1:]

