
import re
from os import listdir, mkdir, remove, walk
from os.path import abspath, exists, isdir, isfile, join, sep
import sys

from . import paths
from .options import parse_args


def create_dest_dir(name, force):
    if not exists(name):
        mkdir(name)
    elif listdir(name) and not force:
        print(
            "Output directory '{}' is not empty, use --force".format(name),
            file=sys.stderr
        )
        sys.exit(2)


def copy_tree(source, dest, transform):

    def get_relative_path(root, name):
        return root[len(name):].strip(sep)

    def make_dir(name):
        '''
        mkdir name. Do nothing if such a dir already exists.
        If name is a file, remove it and create a dir instead.
        Does not handle creation of parent dirs.
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
            make_dir(join(dest, transform(relative_path), transform(subdir)))
        for filename in files:
            copy_file(
                join(dirname, filename),
                join(dest, transform(relative_path), transform(filename))
            )


def create_project(options):
    regex = re.compile('G\{(.+?)\}')
    unmatched_tags = set()

    def replace_tag(match):
        name = match.group(1)
        if name in options:
            return options[match.group(1)]
        else:
            unmatched_tags.add(name)
            return None

    def transform(content):
        return regex.sub(replace_tag, content)

    create_dest_dir(options['name'], options['force'])
    copy_tree(options['template'], options['name'], transform)

    if unmatched_tags:
        print('Warning: Undefined tags in template:', file=sys.stderr)
        for tag in unmatched_tags:
            print('  ' + tag, file=sys.stderr)


def main():
    create_project(parse_args())


if __name__ == '__main__':
    main()

