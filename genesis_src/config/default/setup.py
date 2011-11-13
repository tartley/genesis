from os import listdir, walk
from os.path import isfile, join
import sys


NAME = 'G{name}'
from G{name} import RELEASE


def read_description(filename):
    '''
    Read given textfile and return (first_para, rest_of_document)
    '''
    with open(filename) as fp:
        text = fp.read()
    paras = text.split('\n\n')
    return paras[0], '\n\n'.join(paras[1:])


def get_package_data(topdir, excluded=set()):
    retval = []
    for dirname, subdirs, files in walk(join(NAME, topdir)):
        if any(x in subdirs for x in excluded):
            subdirs.remove(x)
        if any(isfile(f) for f in listdir(dirname)):
            retval.append(join(dirname[len(NAME)+1:], '*.*'))
    return retval


def get_data_files(dest, source):
    from glob import glob
    retval = []
    for dirname, subdirs, files in walk(source):
        retval.append(
            (join(dest, dirname[len(source)+1:]), glob(join(dirname, '*.*')))
        )
    return retval


def get_sdist_config():
    from setuptools import find_packages
    description, long_description = read_description('README.txt')
    return dict(
        name=NAME,
        version=RELEASE,
        description=description,
        long_description=long_description,
        url='G{url}',
        license='G{license}',
        author='G{author}',
        author_email='G{author_email}',
        keywords='',
        packages=find_packages(), #exclude=('*.tests',)),
        data_files=None, #get_data_files('share/doc/' + NAME, 'docs/html'),
        package_data=None, #{ NAME: get_package_data('?') },
        scripts=['G{name}.bat'],
        # see classifiers http://pypi.python.org/pypi?:action=list_classifiers
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: G{license}',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: G{python_version}',
        ],
    )


def create_manifestin(config):
    with open('MANIFEST.in', 'w') as fp:
        for root, branches in config['package_data'].items():
            for branch in branches:
                fp.write('include ' + join(root, branch) + '\n')
        fp.write('include *.txt')
        # TODO: we should also add lines for data_files too.


def main():
    # these imports inside main() so that other scripts can import this file
    # cheaply, to get at its module-level constants like NAME

    # Commented out because I'm not using Distribute.
    # In order to use Distribute, use_setuptools must be called before
    # importing from setuptools:
    #from distribute_setup import use_setuptools
    #use_setuptools()

    from setuptools import setup

    config = get_sdist_config()
    create_manifestin(config)

    if '--verbose' in sys.argv:
        from pprint import pprint
        pprint(config)
    if '--dry-run' in sys.argv:
        return

    setup(**config)


if __name__ == '__main__':
    main()

