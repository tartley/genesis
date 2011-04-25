
from os import chdir, getcwd
from os.path import dirname, exists, expanduser, isdir, isfile, join, normpath
from shutil import copytree, rmtree
from subprocess import Popen
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase

from genesis.paths import CONFIG


TEST_TEMPLATE = 'genesisTestTemplate'
TEST_DIR = dirname(__file__)


class Basic_operation(TestCase):

    def setUp(self):
        # create a temp directory and cd to it
        self.temp_dir = mkdtemp()
        self.orig_cwd = getcwd()
        chdir(self.temp_dir)

        # create the test template
        source = join(TEST_DIR, TEST_TEMPLATE)
        dest = join(CONFIG, TEST_TEMPLATE)
        if exists(dest):
            rmtree(dest)
        copytree(source, dest)

    def tearDown(self):
        # rm the test template
        rmtree( join(CONFIG, TEST_TEMPLATE) )

        # cd back to original cwd and rm the temp directory
        chdir(self.orig_cwd)
        rmtree(self.temp_dir)

    def run_genesis(self, *params):
        script = join(dirname(__file__), '..', '..', 'genesis-script.py')
        command = [ executable, script ] + list(params)
        process = Popen(command)
        self.assertEqual(process.wait(), 0)


    def test_template_is_copied(self):
        self.run_genesis('--template=%s' % (TEST_TEMPLATE,), 'myproj')

        # genesis creates a 'myproj' dir
        myproj_dir = join(self.temp_dir, 'myproj')
        self.assertTrue( exists(myproj_dir) )

        # ...inside of which is file1 and dir1, containing file2
        self.assertTrue( isfile( join(myproj_dir, 'file1') ) )
        self.assertTrue( isdir( join(myproj_dir, 'dir1') ) )
        self.assertTrue( isfile( join(myproj_dir, 'dir1', 'file2') ) )


