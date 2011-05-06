
import argparse
from os.path import isfile, join
import sys

from . import paths


CONFIG_FILENAME = 'config'


def create_parser():
    '''
    Return parser for command-line args with known names.
    '''
    parser = argparse.ArgumentParser(
        prog='genesis',
        description='Create a new Python project.',
    )
    parser.add_argument('--template', default='default',
        help='Project template to use.'
    )
    parser.add_argument('--config-dir',
        help='Genesis config directory, defaults to ~/.genesis. '
            'This option is used for testing Genesis itself.'
    )
    parser.add_argument('name', nargs='+',
        help='Name of your new project, followed by optional space-separated '
            'name=value pairs.'
    )
    return parser



def parse_config_file(filename):
    '''
    Read the config file, return parsed values as a dict
    '''
    if not isfile(filename):
        return {}

    with open(filename) as fp:
        source = fp.read()
    config_vars = {}
    exec(source, globals(), config_vars)
    return config_vars


class Options():
    '''
    Stores a dict of values such that they can be accessed as instance.key,
    instead of instance['key']
    '''
    def __init__(self, d=None):
        if d:
            self.__dict__.update(d)
    def update(self, d):
        self.__dict__.update(d)
    def __iter__(self):
        return self.__dict__.iteritems()
    def __contains__(self, other):
        return self.__dict__.__contains__(other)

    def __str__(self):
        return (
            '\n  '.join(
                ['{'] +
                [
                    '%s=%s' % (key, value)
                    for key, value in vars(self).items()
                ]
            ) +
            '\n}'
        )

def extract_name(options, parser):
    '''
    Options.name contains list of tags, zero or more of which are name=value
    pairs defining a tag, but exactly one of which is just a 'name', denoting
    the project name that is to be created.
    Remove the name from the list, & return (name, tags).
    '''
    if 'name' not in options:
        sys.stderr.write('Project name not specified.')
        parser.print_usage()
        sys.exit(2)

    names = [o for o in options.name if '=' not in o]
    if len(names) == 0:
        sys.stderr.write('Project name not specified.')
        argparse.ArgumentParser.print_usage(parser)
        sys.exit(2)
    if len(names) > 1:
        msg = 'More than one project name specified (%s)' % (', '.join(names),)
        sys.stderr.write(msg)
        argparse.ArgumentParser.print_usage(parser)
        sys.exit(2)

    options.name.remove(names[0])
    return names[0], options.name


def tags_to_dict(taglist):
    tags = {}
    for tag in taglist:
        pos = tag.find('=')
        tags[tag[:pos]] = tag[pos+1:]
    return tags


def parse_args():
    '''
    Combine args from config file and command line into a single Options
    instance.
    '''
    opts_cmdline = Options()

    parser = create_parser()
    parser.parse_args(namespace=opts_cmdline)
    opts_cmdline.name, taglist = extract_name(opts_cmdline, parser)
    opts_tags = tags_to_dict(taglist)

    # command-line can override location of config file
    if opts_cmdline.config_dir:
        paths.CONFIG = opts_cmdline.config_dir

    opts_file = parse_config_file(join(paths.CONFIG, CONFIG_FILENAME))

    # command-line overrides config file
    result = Options()
    result.update(opts_file)
    result.update(opts_cmdline)
    result.update(opts_tags)
    return result

