
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := G{name}
RELEASE := $(shell python -c "from ${NAME} import RELEASE; print(RELEASE)")


clean:
	rm -rf build dist tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
.PHONY: clean


tags:
	ctags -R ${NAME}
.PHONY: tags


tests:
	python -m unittest discover -v .
.PHONY: tests

test: tests
.PHONY: test


sdist: clean
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist
.PHONY: sdist


register:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet register
.PHONY: register


upload: clean
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist upload
.PHONY: upload


py2exe:
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet py2exe
.PHONY: py2exe


# runsnake is a GUI visualiser for the output of cProfile
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	python -O -m cProfile -o profile.out ${NAME}
	runsnake profile.out
.PHONY: profile

