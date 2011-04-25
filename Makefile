
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := genesis
RELEASE := $(shell python -c "from ${NAME} import RELEASE; print(RELEASE)")
SCRIPT := $(shell python -c "from setup import SCRIPT; print(SCRIPT)")


clean:
	rm -rf build dist tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
.PHONY: clean


tags:
	ctags -R ${NAME}
.PHONY: tags


# runsnake is a GUI profile visualiser, very useful.
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	python -O -m cProfile -o profile.out ${SCRIPT}
	runsnake profile.out
.PHONY: profile


tests:
	python -m unittest discover -v .
.PHONY: tests


sdist:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist
	rm -rf ${NAME}.egg-info
.PHONY: sdist


register:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist register
	rm -rf ${NAME}.egg-info
.PHONY: register


upload:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist register upload
	rm -rf ${NAME}.egg-info
.PHONY: upload


py2exe:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet py2exe
	rm -rf ${NAME}.egg-info
.PHONY: py2exe

