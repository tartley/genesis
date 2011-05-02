
import argparse
import os
from os.path import abspath, exists, isdir, isfile, join, sep
from shutil import copyfile
import sys

from .paths import CONFIG


def parse_known_args():
    '''
    Parse command-line args with known names.
    '''
    parser = argparse.ArgumentParser(
        description='Create a new Python project.'
    )
    parser.add_argument('--template', type=str, help='Project template to use.')
    return parser.parse_known_args()


def parse_positional_args(options, args):
    '''
    Parse positional args and args with unknown names, which should be used to
    define template tags.
    '''
    # parse the only positional arg, project name
    for arg in args:
        if not arg.startswith('-'):
            args.remove(arg)
            assert not hasattr(options, 'name')
            options.name = arg

    return options, args


def parse_remaining_args(options, args):
    '''
    Any remaining args, unrecognized by argparse parser, have been specified by
    the user to be used as search-and-replace terms on the tags within the
    project template.
    '''
    while args:
        arg = args.pop(0)
        assert arg.startswith('--')
        arg = arg[2:]
        split = arg.find('=')
        if split > -1:
            key = arg[:split]
            value = arg[split + 1:]
        else:
            key = arg
            value = ''
            if args:
                value = args.pop(0)
                assert not value.startswith('-')
        setattr(options, key, value)

    return options


def parse_args():
    '''
    Parse command-line args, returned in an argparse.Namespace object.
    '''
    return (
        parse_remaining_args(
            *parse_positional_args(
                *parse_known_args()
            )
        )
    )


def create_dest_dir(name):
    #if exists( name ):
        #if listdir( options.name ):
            #print(
                #"Directory '%s' is not empty, use --force" % (options.name,),
                #file=sys.stdout
            #)
    os.mkdir(name)


def copy_tree(source, dest, options):

    def get_relative_path(root, name):
        return root[len(name):].strip(sep)

    def make_dir(name):
        '''
        if name is a dir, do nothing.
        If name is a file, remove it and create a dir instead.
        If name does not exist, create a dir.
        '''
        name = abspath(name)
        if isfile(name):
            os.remove(name)
        elif not isdir(name):
            os.mkdir(name)

    def copy_file(source, dest):
        '''
        Copy file source to destination, replacing template tags as we copy.
        '''
        with open(source) as source_fp:
            with open(dest, 'w') as dest_fp:
                content = source_fp.read()
                for name, value in vars(options).items():
                    content = content.replace('G{' + name + '}', value)
                dest_fp.write(content)

    for dirname, subdirs, files in os.walk(source):
        relative_path = get_relative_path(dirname, source)
        for subdir in subdirs:
            make_dir(join(dest, relative_path, subdir))
        for filename in files:
            copy_file(
                join(dirname, filename),
                join(dest, relative_path, filename)
            )


def create_project(options):
    create_dest_dir(options.name)
    copy_tree( join(CONFIG, options.template), options.name, options)


def main():
    create_project( parse_args() )


if __name__ == '__main__':
    main()

