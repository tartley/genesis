Genesis is a command-line tool to create new Python projects.

When invoked, it copies files and directories from a project template,
doing several search-and-replace operations on the copied files to insert
your project's name, the project author's name, etc.

One standard project template is provided built-in to Genesis, but you can
also supply your own.

Dependencies
------------

  * Tested on Ubuntu and Windows XP
  * Python 3.2


Usage
-----

::

    genesis <options> <projectname>

This creates a directory named 'projectname' if it doesn't already exist,
containing your new project. <options> may include::

    --template=T
        T defaults to 'default', or accepts the name of any template directory
        in your ~/.genesis directory.
    --license=L
        Determines what LICENSE.txt file to create. L defaults to bsd, or
        accepts apache, bsd, gpl, lgpg, mit, python.
    --txt-extension=.txt
        Defaults to .txt on Windows, nothing otherwise.

    --ANYTHING=VALUE
        All specified flags are used to search-and-replace for template tags
        in the template files. See section 'Templates.'

See the section 'Config file' to save you having to type these on the
command-line every time.

Values can be specified either as --foo=bar or as --foo bar.

Minuses and underscores in the name of command-line flags are equivalent, e.g.
Use either --txt-extensions or --txt_extensions.


Config file
-----------

To save having to type values such as ``--author=foo`` on the command-line
every time, you can put them into config file ``~/.genesis/genesis.config``.
For example, a config file might contain::

    author = 'Jonathan Hartley'

This is a Python3.2 syntax file (although it has no .py extension) in which you
can assign a value to variables with the same name as any command-line flag.
Minuses cannot be used in Python identifiers (on the left hand side of the
equals sign), so use underscores instead.


Templates
---------

Project templates are directories stored inside ``~/.genesis``.

When Genesis copies a template, it replaces any occurences of ``G{foo-bar}``,
known as a `template tag`, with the value specified in command-line flag
``--foo-bar=X``, or by the value of ``foo_bar='X'`` assigned in your config
file. Values from the command-line override the config file.

Occurrences of template tags in file or directory names are also replaced.

A warning is issued for any template tag for which neither the config file
nor the command-line specify a value.

Minuses and underscores are equivalent in the name of template tags. E.g.
when Genesis searches-and-replaces 'G{foo-bar}', it also searches and replaces
'G{foo_bar}' at the same time.


The Default Project Template
----------------------------

Projects created by Genesis 'default' template support the following:

**Create a source distribution**

::

    python setup.py sdist

This uses the first paragraph from your README as your project's
description, and the remainder of the README as the long_description. The
Cheese Shop expects these to be in RestructuredText format like this README
is.

**Register on The Cheese Shop (PyPI)**

::

    python setup.py register

**Upload source distribution to the Cheese Shop (PyPI)**

::

    python setup.py sdist register upload

**Create a Windows binary**

::

    python setup.py py2exe

**Makefile**

A Makefile is created to abbreviate the above commands (make sdist, etc), and
also supports the following targets:

  clean
    Deletes .pyo .pyc, tags. Requires ctags to be on the path.
  profile
    Requires RunSnakeRun, see Makefile for details.

The Makefile can be used on Windows by, for example, having Cygwin binaries
on your PATH.


Known Issues
------------

Very early in development - nothing works yet.

Assumes your project is BSD license, which it puts into your project's
LICENSE.txt file.


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's excellent book
`Expert Python Programming`, which improved the way I work with Python every
day.
