
from os.path import expanduser, join, sep

HOME = expanduser('~')
USER_CONFIG = join(HOME, '.genesis')


def tilde_encode(filename):
    home = expanduser('~')
    if filename.startswith(home):
        return '~' + sep + filename[len(home)+1:]

