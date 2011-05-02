
import argparse


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


