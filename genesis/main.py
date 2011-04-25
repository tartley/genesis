
import argparse
from os import mkdir
from os.path import exists, join
from shutil import copytree
import sys

from .paths import CONFIG


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create a new Python project.'
    )
    parser.add_argument('name', type=str, help='Name of your new project')
    parser.add_argument('--template', type=str, help='Project template to use.')
    return parser.parse_args()


def create_project( options ):
    #if exists( options.name ):
        #if listdir( options.name ):
            #print(
                #"Directory '%s' is not empty, use --force" % (options.name,),
                #file=sys.stdout
            #)
        #else:
            # target dir is empty, so we can safely delete it
            #rm options.name
    copytree( join(CONFIG, options.template), options.name)


def main():
    create_project( parse_args() )


if __name__ == '__main__':
    main()

