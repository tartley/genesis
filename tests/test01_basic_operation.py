
from os import chdir, getcwd
from os.path import dirname, join, normpath
from shutil import rmtree
from subprocess import Popen
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase

class Basic_operation(TestCase):

    def setUp(self):
        self.temp_dir = mkdtemp()
        self.orig_dir = getcwd()
        chdir(self.temp_dir)

    def tearDown(self):
        chdir(self.orig_dir)
        rmtree(self.temp_dir)

    def test_template_is_copied(self):
        script = normpath(join(dirname(__file__), '..', 'genesis.py'))
        process = Popen([executable, script, 'myproj'])
        self.assertEqual(process.wait(), 0)

