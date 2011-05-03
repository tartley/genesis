
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
        description='Create a new Python project.',
        epilog="Plus arbitrary options of the form '--foo=bar', which are "
            "used to search-and-replace tags such as 'G{foo}' in the "
            "copied project template."
    )
    parser.add_argument(
        '--template', type=str, default='default',
        help='Project template to use.'
    )
    parser.add_argument(
        '--config-dir', type=str,
        help='Genesis config directory, defaults to ~/.genesis. '
            'This option is only useful for testing Genesis itself.'
    )
    #parser.add_argument('name', type=str, help='Name of your new project')
    return parser


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
    def __contains__(self, other):
        return other in self.__dict__
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


def parse_args():
    '''
    Combine args from config file and command line into a single Options
    instance.
    '''
    parser = create_parser()
    command_line_opts = parse_remaining_args(
        *parse_positional_args(
            *parser.parse_known_args()
        )
    )

    # command-line can override location of config dir
    if command_line_opts.config_dir:
        paths.CONFIG = command_line_opts.config_dir
    config_file_opts = parse_config_file(join(paths.CONFIG, CONFIG_FILENAME))

    # command-line overrides config file
    options = Options(config_file_opts)
    options.update(vars(command_line_opts))

    if 'name' not in options:
        parser.print_help()
        sys.exit(2)

    return options

