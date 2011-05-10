
import argparse
from os.path import isdir, isfile, join
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
    parser.add_argument('--force', action='store_true', default=False,
        help='Force writing to an existing non-empty output dir.'
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
    def update(self, d):
        self.__dict__.update(d)
    def __str__(self):
        return (
            '\n  '.join(
                ['{'] +
                [
                    '{}={}'.format(key, value)
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
        print('Project name not specified.', file=sys.stderr)
        parser.print_usage()
        sys.exit(2)

    names = [o for o in options.name if '=' not in o]
    if len(names) == 0:
        print('Project name not specified.', file=sys.stderr)
        argparse.ArgumentParser.print_usage(parser)
        sys.exit(2)
    if len(names) > 1:
        msg = 'More than one project name specified ({})'.format(
            ', '.join(names)
        )
        print(msg, file=sys.stderr)
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


def locate_template(name):
    possibles = [
        paths.USER_CONFIG,
        paths.PACKAGE_CONFIG,
    ]
    for possible in possibles:
        template_dir = join(possible, name)
        if isdir(template_dir):
            return template_dir

    print(
        "Template '{}' not found in {}.".format(
            name, paths.tilde_encode(possibles[0])
        ),
        file=sys.stderr
    )
    sys.exit(2)


def parse_args():
    '''
    Combine args from config file and command line into a single Options
    instance.
    '''
    parser = create_parser()
    opts_cmdline = parser.parse_args()
    opts_cmdline.name, taglist = extract_name(opts_cmdline, parser)
    opts_tags = tags_to_dict(taglist)

    # command-line can override location of config file
    if opts_cmdline.config_dir:
        paths.USER_CONFIG = opts_cmdline.config_dir

    opts_file = parse_config_file(join(paths.USER_CONFIG, CONFIG_FILENAME))

    # command-line name=value tags override command-line options, and
    # both override the config file
    result = Options()
    result.update(opts_file)
    result.update(vars(opts_cmdline))
    result.update(opts_tags)

    result.template = locate_template(result.template)

    return result

