
from os import chdir, getcwd, mkdir
from os.path import (
    dirname, exists, expanduser, isdir, isfile, join, normpath, relpath
)
from shutil import copytree, rmtree
from subprocess import PIPE, Popen
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase

from genesis.paths import CONFIG


SCRIPT = 'genesis-script.py'
TEST_TEMPLATE = 'testTemplate'
TEST_DIR = dirname(__file__)
TEST_CONFIG = 'test_config_dir'


def read_file(filename):
    with open(filename) as fp:
        return fp.read()

def str_decode(s):
    return bytes(s).decode('unicode_escape')


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


    def run_genesis(self, *params):
        script = normpath(
            join(dirname(__file__), '..', '..', SCRIPT)
        )
        process = Popen(
            [ executable, script ] +
            [ '--config-dir={}'.format(join(TEST_DIR, TEST_CONFIG)) ] +
            list(params),
            stdout=PIPE,
            stderr=PIPE,
        )
        out, err = process.communicate()
        return process.returncode, out, err


    def assert_genesis_runs_ok(self):
        exitval, out, err = self.run_genesis(
            '--template={}'.format(TEST_TEMPLATE),
            'myproj',
            'author=Jonathan Hartley',
        )
        self.assertEqual(err, b'', str_decode(err))
        self.assertEqual(out, b'', str_decode(out))
        self.assertEqual(exitval, 0)

        # genesis creates a 'myproj' dir
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertTrue( exists(myproj_dir) )

        # ...inside of which is file1 and dir1, containing file2
        self.assertTrue( isfile( join(myproj_dir, 'file1') ) )
        self.assertTrue( isdir( join(myproj_dir, 'dir1') ) )
        self.assertTrue( isfile( join(myproj_dir, 'dir1', 'file2') ) )


    def assert_genesis_gives_error(self, *args, expected_err=None):
        exitval, out, err = self.run_genesis(*args)
        if expected_err:
            self.assertTrue(expected_err in str(err), str_decode(err))
        else:
            self.assertEqual(err, b'', str_decode(err))
        self.assertEqual(out, b'', str_decode(out))
        self.assertEqual(exitval, 2)


    def test_template_is_copied_and_tags_expanded(self):
        self.assert_genesis_runs_ok()

        # file1 has had G{name} replaced by 'myproj',
        # and 'G{author} replaced by 'Jonathan Hartley',
        # as specified on the command-line
        myproj_dir = join(self.temp_dir, 'myproj')
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


    def test_zero_args_shows_usage(self):
        self.assert_genesis_gives_error(expected_err='usage:')
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertFalse( exists(myproj_dir) )


    def test_existing_empty_dir_is_filled(self):
        mkdir('myproj')
        self.assert_genesis_runs_ok()


    def test_existing_full_dir_raises_an_error(self):
        mkdir('myproj')
        with open(join('myproj', 'somefile'), 'w') as fp:
            pass
        self.assert_genesis_gives_error(
            '--template={}'.format(TEST_TEMPLATE),
            'myproj',
            'author=Jonathan Hartley',
            expected_err="Output directory 'myproj' is not empty, use --force",
        )


    def DONTtest_list_unreplaced_tags(self):
        self.fail()

    def DONTtest_force_arg_to_overwrite_non_empty_dirs(self):
        self.fail()

