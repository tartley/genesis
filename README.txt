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

    --template (defaults to 'default'. Other acceptable values are the names
                of template directories in your ~/.genesis directory)
    --license, determines what LICENSE.txt file to create. Defaults to bsd.
        Accepts apache, bsd, gpl, lgpg, mit, python.
    --txt-extension, defaults to .txt on Windows, nothing otherwise.

All the above flags, together with any other arbitrary ones specified by the
user, are used to search-and-replace tags in the copied template files. For
example, any occurences of 'G{author-email}' in the template files are
replaced by the value of --author-email=X specified on the command-line.

Values can be specified either as --foo=bar or as --foo bar.

Minuses in names of flags may alternatively be specified as underscores,
(e.g. --author_email)

See the 'Config file' section to save you having to type these on the
command-line every time.


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
time, you can put them into ~/.genesis/genesis.config. This is a python syntax
file (although it has no .py extension) in which you can assign a value to
variables with the same name as any command-line flag. For example::

    author = 'Jonathan Hartley'


Creating your own templates
---------------------------

Project templates are directories stored inside ~/.genesis.

When Genesis copies a template, it replaces any occurences of 'G{foo-bar}' are
replaced by the value given in command-line flag --foo-bar=X, or by the value
of foo_bar assigned in your config file. Note that minuses in command line
flags are underscores in the config file.

Occurrences of G{foo} in file or directory names are also replaced.


Known Issues
------------

Very early in development - doesn't yet work.

Assumes it is cool to put BSD license.txt into newly created project. I must
add support for other licenses.


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's excellent book
'Expert Python Programming', which improved the way I work with Python every
day.

