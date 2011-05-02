
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


TEST_TEMPLATE = 'genesisTestTemplate'
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

    def DONTtests_should_use_fake_config_dir_instead_of_copying_a_test_template(self):
        self.fail()

    def DONTtest_list_option_lists_tags_in_template(self):
        self.fail()

    def DONTtest_force_arg_to_overwrite_non_empty_dirs(self):
        self.fail()

    def DONTtest_accept_minuses_or_underscores(self):
        # If you want something to display as 'pos-arg1' and be stored as
        # 'pos_arg1', you should use
        # add_argument('pos_arg1', metavar='pos-arg1')
        pass

