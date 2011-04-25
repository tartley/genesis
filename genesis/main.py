
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description='Create a new Python project.'
    )
    parser.add_argument('name', type=str, help='Name of your new project')
    return parser.parse_args()


def create_project( options ):
    if not os.path.exists( options.name ):
        os.mkdir( options.name )
    elif listdir( options.name ):
        print(
            "Directory '%s' is not empty, use --force" % (options.name,),
            file=sys.stdout
        )


def main():
    create_project( parse_args() )


if __name__ == '__main__':
    main()

