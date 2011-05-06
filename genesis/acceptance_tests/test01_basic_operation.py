
from os import chdir, getcwd
from os.path import (
    dirname, exists, expanduser, isdir, isfile, join, normpath, relpath
)
from shutil import copytree, rmtree
from subprocess import Popen
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase

from genesis.paths import CONFIG


TEST_TEMPLATE = 'testTemplate'
TEST_DIR = dirname(__file__)


def read_file(filename):
    with open(filename) as fp:
        return fp.read()


class Basic_operation(TestCase):

    def setUp(self):
        # create a temp directory and cd to it
        self.temp_dir = mkdtemp()
        self.orig_cwd = getcwd()
        chdir(self.temp_dir)


    def tearDown(self):
        # cd back to original cwd and rm the temp directory
        chdir(self.orig_cwd)
        rmtree(self.temp_dir)


    def _run_genesis(self, *params):
        script = normpath(
            join(dirname(__file__), '..', '..', 'genesis-script.py')
        )
        process = Popen(
            [ executable, script ] +
            [ '--config-dir=%s' % (join(TEST_DIR, 'testConfigDir'),) ] +
            list(params)
        )
        return process.wait()

    def run_genesis_ok(self, *params):
        exitval = self._run_genesis(*params)
        self.assertEqual(exitval, 0)

    def run_genesis_fail(self, *params):
        exitval = self._run_genesis(*params)
        self.assertEqual(exitval, 2)


    def test_template_is_copied_and_tags_expanded(self):
        self.run_genesis_ok(
            '--template=%s' % (TEST_TEMPLATE,),
            'myproj',
            'author=Jonathan Hartley',
        )

        # genesis creates a 'myproj' dir
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertTrue( exists(myproj_dir) )

        # ...inside of which is file1 and dir1, containing file2
        self.assertTrue( isfile( join(myproj_dir, 'file1') ) )
        self.assertTrue( isdir( join(myproj_dir, 'dir1') ) )
        self.assertTrue( isfile( join(myproj_dir, 'dir1', 'file2') ) )

        # file1 has had G{name} replaced by 'myproj',
        # and 'G{author} replaced by 'Jonathan Hartley',
        # as were specified on the command-line
        self.assertEqual(
            read_file(join(myproj_dir, 'file1')),
            (
                'Project name: myproj\n'
                'Author name: Jonathan Hartley\n'
                '\n'
            )
        )

        # file2 has had G{author_email} replaced by 'tartley@tartley.com',
        # as specified in the config file
        self.assertEqual(
            read_file(join(myproj_dir, 'dir1', 'file2')),
            (
                'Author email: tartley@tartley.com\n'
                '\n'
            )
        )

    # TODO
    # Putting 'name' positional arg into argparse parser uses the first
    # unrecognised optional arg (e.g. --author) to populate it. Removing
    # 'name' from argparse, to be handled by parse_positional_args, means it
    # is missing from the auto-generated usage text.

    def test_zero_args_shows_usage(self):
        self.run_genesis_fail()

    def DONTtest_list_unreplaced_tags(self):
        self.fail()

    def DONTtest_force_arg_to_overwrite_non_empty_dirs(self):
        self.fail()

