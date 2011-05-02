
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


    def run_genesis(self, *params):
        script = normpath(
            join(dirname(__file__), '..', '..', 'genesis-script.py')
        )
        process = Popen(
            [ executable, script ] +
            [ '--config-dir=%s' % (join(TEST_DIR, 'testConfigDir'),) ] +
            list(params)
        )
        self.assertEqual(process.wait(), 0)


    def test_template_is_copied_and_tags_expanded(self):
        self.run_genesis(
            '--template=%s' % (TEST_TEMPLATE,),
            '--author=Jonathan Hartley',
            'myproj'
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
        x = read_file(join(myproj_dir, 'file1'))
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


    def DONTtest_list_unreplaced_tags(self):
        self.fail()

    def DONTtest_force_arg_to_overwrite_non_empty_dirs(self):
        self.fail()

