
from os import chdir, getcwd, mkdir
from os.path import (
    dirname, exists, expanduser, isdir, isfile, join, normpath, relpath
)
from shutil import copytree, rmtree
from subprocess import PIPE, Popen
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase

from genesis import paths


SCRIPT = 'genesis.bat'
TEST_TEMPLATE = 'test_template'
TEST_DIR = dirname(__file__)
TEST_CONFIG = 'fake_config'


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
            [ script ] +
            [ '--config-dir=' + join(TEST_DIR, TEST_CONFIG) ] +
            list(params),
            stdout=PIPE,
            stderr=PIPE,
        )
        out, err = process.communicate()
        return process.returncode, out, err


    def assert_genesis_runs(self, *args, err=None, exit=0):
        exitval, outval, errval = self.run_genesis(*args)
        if err is not None:
            self.assertIn(bytes(err, 'utf-8'), errval, str_decode(errval))
        else:
            self.assertEqual(errval, bytes('', 'utf-8'), str_decode(errval))
        self.assertEqual(outval, b'', str_decode(outval))
        self.assertEqual(exitval, exit)


    def assert_test_template_files_created(self):
        # genesis should create a 'myproj' dir
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertTrue( exists(myproj_dir) )

        # ...inside of which is file1 and dir1, containing file2
        self.assertTrue( isfile( join(myproj_dir, 'file1') ) )
        self.assertTrue( isdir( join(myproj_dir, 'dir1') ) )
        self.assertTrue( isfile( join(myproj_dir, 'dir1', 'file2') ) )


    def assert_default_template_files_created(self):
        # genesis creates a 'myproj' dir
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertTrue( exists(myproj_dir) )

        # ...inside of which is default template files and dirs
        self.assertTrue( isfile( join(myproj_dir, 'CHANGES.txt') ) )
        self.assertTrue( isfile( join(myproj_dir, 'LICENSE.txt') ) )
        self.assertTrue( isfile( join(myproj_dir, 'Makefile') ) )
        self.assertTrue( isfile( join(myproj_dir, 'README.txt') ) )
        self.assertTrue( isfile( join(myproj_dir, 'setup.py') ) )
        self.assertTrue( isfile( join(myproj_dir, 'TODO.txt') ) )


    def test_template_should_be_copied_and_tags_expanded(self):
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            'myproj',
            'author=Jonathan Hartley',
        )
        self.assert_test_template_files_created()

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


    def test_zero_args_should_show_usage(self):
        self.assert_genesis_runs(err='usage:', exit=2)
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertFalse( exists(myproj_dir) )


    def test_existing_empty_dir_is_filled(self):
        mkdir('myproj')
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            'myproj',
            'author=Jonathan Hartley',
        )
        self.assert_test_template_files_created()


    def test_existing_full_dir_should_raise_an_error(self):
        mkdir('myproj')
        with open(join('myproj', 'somefile'), 'w') as fp:
            pass
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            'myproj',
            err="Output directory 'myproj' is not empty, use --force",
            exit=2,
        )


    def test_existing_full_dir_with_force_param_should_be_written_to(self):
        mkdir('myproj')
        with open(join('myproj', 'somefile'), 'w') as fp:
            pass
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            '--force',
            'myproj',
            'author=Jonathan Hartley',
        )


    def test_missing_template_should_raise_error(self):
        self.assert_genesis_runs(
            '--template=non_existant',
            'myproj',
            err="Template 'non_existant' not found in {}.".format(
                paths.tilde_encode(join(TEST_DIR, TEST_CONFIG))
            ),
            exit=2,
        )


    def test_default_template_read_from_package_if_not_in_config_dir(self):
        self.assert_genesis_runs(
            'myproj',
            err='' # ignore error text, best left for separate test
        )
        self.assert_default_template_files_created()


    def test_tags_in_filenames_should_be_replaced(self):
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            'myproj',
            'author=Jonathan Hartley',
        )
        self.assertTrue(  isdir( join('myproj', 'myproj') ) )
        self.assertTrue( isfile( join('myproj', 'myproj', 'myproj.bat') ) )


    def test_undefined_tags_in_template_should_produce_warning(self):
        self.assert_genesis_runs(
            '--template=' + TEST_TEMPLATE,
            'myproj',
            err='Warning: Undefined tags in template:\n  author',
        )


    def DONTtest_list_unreplaced_tags(self):
        self.fail()

