
import argparse
from os.path import join

from . import paths


CONFIG_FILENAME = 'config'


def parse_known_args():
    '''
    Parse command-line args with known names.
    '''
    parser = argparse.ArgumentParser(
        description='Create a new Python project.'
    )
    parser.add_argument('--template', type=str, help='Project template to use.')
    parser.add_argument('--config-dir', type=str, help='Genesis config directory, defaults to ~/.genesis. This option is only useful for testing Genesis itself.')
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


class Options():
    '''
    Stores a dict of values such that they can be accessed as instance.key,
    instead of instance['key']
    '''
    def __init__(self, d):
        self.__dict__.update(d)
    def update(self, d):
        self.__dict__.update(d)
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

def parse_config_file(filename):
    '''
    Read the config file,
    return an Options instance containing the parsed values.
    '''
    with open(filename) as fp:
        source = fp.read()
    config_vars = {}
    exec(source, globals(), config_vars)
    return Options(config_vars)


def parse_args():
    '''
    Combine args from config file and command line into a single Options
    instance.
    '''
    command_line_options = (
        parse_remaining_args( *parse_positional_args( *parse_known_args() ) )
    )

    # command-line can override location of config dir
    if command_line_options.config_dir:
        paths.CONFIG = command_line_options.config_dir
    config_file_options = parse_config_file(join(paths.CONFIG, CONFIG_FILENAME))

    # command-line overrides config file
    config_file_options.update(vars(command_line_options))

    return config_file_options

