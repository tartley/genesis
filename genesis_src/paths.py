from os import environ
from os.path import dirname, join, sep


HOME = environ['HOME']
USER_CONFIG = join(HOME, '.genesis')

SOURCE = dirname(__file__)
PACKAGE_CONFIG = join(SOURCE, 'config')


def tilde_encode(filename):
    if filename.startswith(HOME):
        return '~' + sep + filename[len(HOME)+1:]

