Genesis is a command-line tool to create new Python projects.

When invoked, it copies files and directories from a project template,
doing several search-and-replace operations on the copied files to insert
your project's name, the project author's name, etc.

One standard project template is provided built-in to Genesis, but you can
also supply your own.

Dependencies
------------

  * Tested on Ubuntu and Windows XP
  * Python 3.2 or 2.7


Usage
-----

::

    genesis <options> <projectname>

This creates a directory named 'projectname' if it doesn't already exist,
containing your new project. <options> may include::

    --template (defaults to 'default')

Any of these options can also be specified in the configuration file, described
below, to save you having to type them on the command-line every time.


Features
--------

Create a source distribution::

    python setup.py sdist

This uses the first paragraph from your README as your project's description,
and the remainder of the README as the long_description. The Cheese Shop
expects these to be in RestructuredText format like this README is.

Register on The Cheese Shop (PyPI)::

    python setup.py register

Upload source distribution to the Cheese Shop (PyPI)::

    python setup.py sdist register upload

Create a Windows binary::

    python setup.py py2exe

A Makefile is created to abbreviate the above commands (make sdist, etc), and
also supports the following targets::

    clean (delete .pyo .pyc, 
    tags (requires ctags to be on the path)
    linecount (counts non-blank lines of code)
    profile (requires RunSnakeRun, see Makefile for details)

I use the Makefile both on Ubuntu and on Windows by having Cygwin binaries on
my PATH.


Config file
-----------

To save having to type values such as '--author=foo' on the command-line every
time, you can put them into ~/.genesisrc. This is a python syntax file
(although it has no .py extension) in which you can assign a value to
variables with the same name as any command-line flag. For example::

    author = 'Jonathan Hartley'


Creating your own templates
---------------------------

Templates are simply directories stored inside ~/.genesis.

Any occurences of template tags of the form '${foo}' are replaced by the value
given in command-line flag --foo=X, or by the value for foo='X' given in
your config file.

Occurrences of ${foo} in file or directory names are also replaced.


Known Issues
------------

Very early in development - doesn't yet work.


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's excellent book
'Expert Python Programming', which improved the way I work with Python every
day.

