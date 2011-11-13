
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := genesis
SOURCE := ${NAME}_src
RELEASE := $(shell python -c "from ${SOURCE} import RELEASE; print(RELEASE)")
PYTHON := python3


clean:
	rm -rf build dist tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
.PHONY: clean


tags:
	ctags -R ${SOURCE}
.PHONY: tags


test:
	${PYTHON} -m unittest discover -v .
.PHONY: test


sdist: clean
	rm -rf dist/${NAME}-${RELEASE}.* build
	${PYTHON} setup.py --quiet sdist
.PHONY: sdist


register:
	rm -rf dist/${NAME}-${RELEASE}.* build
	${PYTHON} setup.py --quiet register
.PHONY: register


upload: clean
	rm -rf dist/${NAME}-${RELEASE}.* build
	${PYTHON} setup.py --quiet sdist upload
.PHONY: upload


py2exe:
	rm -rf dist/${NAME}-${RELEASE}.* build
	${PYTHON} setup.py --quiet py2exe
.PHONY: py2exe


# runsnake is a GUI visualiser for the output of cProfile
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	${PYTHON} -O -m cProfile -o profile.out ${NAME}
	runsnake profile.out
.PHONY: profile

