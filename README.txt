Genesis is a command-line tool to create new Python projects.

When invoked, it copies files and directories from a project template,
doing several search-and-replace operations on the copied files to insert
your project's name, the project author's name, etc.

One default project template is provided built-in to Genesis, but you can
also supply your own.

Note that this README describes some features which are not yet implemented.
See 'Known Issues' below.


Dependencies
------------

  * Tested on Ubuntu and Windows XP
  * Python 3.2


Usage
-----

::

    genesis [<options>] <projectname> [<name>=<value>...]

This creates a directory named *projectname*, if it doesn't already exist,
containing your new project. <Options> may include any of:

    --template=T
        Template to use. T defaults to 'default'. Valid values are the name of
        any template directory stored within your '~/.genesis' directory.
    --license=L
        Uses license file 'L' from ~/.genesis/licenses. Also useful as a
        template tag: ``G{license}`` anywhere else in your template will be
        replaced with the name of your license.
    --force
        Required to create a new project in a non-empty directory, overwriting
        any files or dirs with the same name as template content.
    --config-dir=C
        Use C as your config dir instead of ~/.genesis. Used for testing
        Genesis itself during development.

In addition, the command line can include any number of space-separated
``name=value`` pairs, which are used to search-and-replace tags of the form
``G{name}`` within the copied template.

For example, ``author_email=me@example.com`` on the command-line will cause
``G{author_email}`` anywhere in the template to be replaced with
'me@example.com' in the created project.

``<Projectname>`` should not contain any equals characters - this is the only
feature that distinguishes it from ``name=value`` pairs.


Missing tag values
------------------

If the template contains any ``G{name}`` tags which do not have a value defined
on the command-line nor in the config file, then a warning will be issued,
e.g::

    Undefined: G{license} in path/file.py, line 65

The project that is created will still have the text ``G{license}`` in it at
this location. To fix this, you should define a value for ``license`` either on
the command line or in your config file. Then either delete the generated
project directory and re-run genesis, or else just re-run it with the
``--force`` command-line flag, so that it is forced to overwrite the previously
generated project.


Config file
-----------

The config file, ``~/.genesis/genesis.config``, is a Python3.2 syntax file,
although it has no .py extension. In it values can be assigned to
variables which behave just like flags or name-value pairs on the command-line.
For example, a config file might contain::

    template = 'my_favourite'
    author = 'Jonathan Hartley'
    
This is equivalent to specifying
``--template=my_favourite author=Jonathan\ Hartley`` on the command-line.

Values in the config file are overriden by the command-line.

If your template contains tags with names which are not valid Python variable
names, you will not be able to specify those tags' values in the config file.


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

The Makefile can be used on Windows by having Cygwin binaries on your PATH.


Defining your own templates
---------------------------

Create a directory under ``~/.genesis``. Fill it with the files and directories
you'd like to start your project with. Insert tags into the template files
of the form ``G{name}``. Now you can create a new project using this template
using::

    genesis --template <mytemplate> <projectname>

Where ``<mytemplate>`` is the name of the directory you created. To make this
type of template the default, add a line to your config file::

    template = '<mytemplate>'

Now you need only issue the command-line::

    genesis <projectname>


Known Issues
------------

If Genesis doesn't find the default template in ~/.genesis, it should look
in the package directory, so that it works from source or out of box on
install, without having to copy anything to ~/.genesis.

Undefined tag values are not reported.

--license not implemented. Assumes your project is BSD license.

Not actually tested on Ubuntu

No binaries are available, which makes Genesis unusable unless you use Python
3.2.

The config file is parsed using 'eval'. I'm not smart enough to know whether
this is a security problem.


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's highly
recommended book `Expert Python Programming`, which improved the way I work
with Python every day.

