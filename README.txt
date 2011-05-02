Genesis is a command-line tool to create new Python projects.

When invoked, it copies files and directories from a project template,
doing several search-and-replace operations on the copied files to insert
your project's name, the project author's name, etc.

One default project template is provided built-in to Genesis, but you can
also supply your own.

Note that this README describes some features which are not yet implemented.


Dependencies
------------

  * Tested on Ubuntu and Windows XP
  * Python 3.2


Usage
-----

::

    genesis <options> <projectname>

This creates a directory named *projectname*, if it doesn't already exist,
containing your new project. <Options> may include any name-value pair:

    --ANYTHING=VALUE
        All such options are used to search and replace in the content and
        filenames of copied template files. For example, any occurrence of
        'G{ANYTHING}' within the template files will be replaced with 'VALUE'.
        See section 'Templates.'

In addition, the following command-line options also have special meanings:

    --template=T
        Template to use. T defaults to 'default'. Valid values are the name of
        any template directory stored within your '~/.genesis' directory.
    --license=L
        What license to use for your new project. This determines what
        LICENSE.txt file to create. Valid values of L include the name of any
        file stored in your '~/.genesis/licenses' directory.

See the section *Config file* to set default values for command line flags.

Values can be specified either as ``--foo=bar`` or as ``--foo bar``.

Minuses and underscores in the name of command-line flags are equivalent. E.g.
``--txt-extensions`` and ``--txt_extensions`` are equivalent.


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

Assumes your project is BSD license.


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's excellent book
`Expert Python Programming`, which improved the way I work with Python every
day.

