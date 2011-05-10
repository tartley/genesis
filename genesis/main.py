
from os import listdir, mkdir, remove, walk
from os.path import abspath, exists, expanduser, isdir, isfile, join, sep
from sys import exit, stderr

from . import paths
from .options import parse_args


def create_dest_dir(name, force):
    if not exists(name):
        mkdir(name)
    elif listdir(name) and not force:
        print(
            "Output directory '{}' is not empty, use --force".format(name),
            file=stderr
        )
        exit(2)


def copy_tree(source, dest, transform):

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
            remove(name)
        elif not isdir(name):
            mkdir(name)

    def copy_file(source, dest):
        '''
        Copy file source to destination, replacing template tags as we copy.
        '''
        with open(source) as source_fp:
            with open(dest, 'w') as dest_fp:
                dest_fp.write( transform( source_fp.read() ) )

    for dirname, subdirs, files in walk(source):
        relative_path = get_relative_path(dirname, source)
        for subdir in subdirs:
            make_dir(join(dest, relative_path, subdir))
        for filename in files:
            copy_file(
                join(dirname, filename),
                join(dest, relative_path, filename)
            )


def create_project(options):
    def transform(content):
        for name, value in vars(options).items():
            content = content.replace('G{' + name + '}', str(value))
        return content

    create_dest_dir(options.name, options.force)
    copy_tree( join(paths.USER_CONFIG, options.template), options.name, transform)


def main():
    options = parse_args()
    create_project(options)


if __name__ == '__main__':
    main()

