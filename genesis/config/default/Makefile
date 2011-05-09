
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


VERSION := $(shell python -c "from G{NAME} import __version__; print __version__")


clean:
	rm -rf build dist tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
.PHONY: clean


tags:
	ctags -R G{NAME}
.PHONY: tags


# runsnake is a GUI profile visualiser, very useful.
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	python -O -m cProfile -o profile.out G{name}
	runsnake profile.out
.PHONY: profile


sdist:
	rm -rf dist/G{NAME}-${VERSION}.* build
	python setup.py --quiet sdist
	rm -rf G{NAME}.egg-info
.PHONY: sdist


register:
	rm -rf dist/G{NAME}-${VERSION}.* build
	python setup.py --quiet sdist register
	rm -rf G{NAME}.egg-info
.PHONY: register


upload:
	rm -rf dist/G{NAME}-${VERSION}.* build
	python setup.py --quiet sdist register upload
	rm -rf G{NAME}.egg-info
.PHONY: upload


py2exe:
	rm -rf dist/G{NAME}-${VERSION}.* build
	python setup.py --quiet py2exe
	rm -rf G{NAME}.egg-info
.PHONY: py2exe

