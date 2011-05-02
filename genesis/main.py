
import os
from os.path import abspath, exists, isdir, isfile, join, sep

from . import paths
from .options import parse_args


def create_dest_dir(name):
    #if exists( name ):
        #if listdir( options.name ):
            #print(
                #"Directory '%s' is not empty, use --force" % (options.name,),
                #file=sys.stdout
            #)
    os.mkdir(name)


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
            os.remove(name)
        elif not isdir(name):
            os.mkdir(name)

    def copy_file(source, dest):
        '''
        Copy file source to destination, replacing template tags as we copy.
        '''
        with open(source) as source_fp:
            with open(dest, 'w') as dest_fp:
                dest_fp.write( transform( source_fp.read() ) )

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
    def transform(content):
        for name, value in vars(options).items():
            content = content.replace('G{' + name + '}', value)
        return content

    create_dest_dir(options.name)
    copy_tree( join(paths.CONFIG, options.template), options.name, transform)


def main():
    create_project( parse_args() )


if __name__ == '__main__':
    main()

