PDFBOOK:=book_output/simbook.pdf
HTMLBOOK:=book_output/coalescent-simulation.html

RMDFILES:=index.Rmd $(shell find chapters -type f -name '*.Rmd')
BIBFILES:=chapters/simbook.bib
PYLISTINGS:=$(shell find chapters -type f -name '*.py' | grep listings)
PYTHONPACKAGE:=$(shell find ../simbook -type f -name '*.py' | grep -v __init__)
PYTHONFIGS=hudson1990.png migration.png msprime_scaling.png

all: ${PDFBOOK} ${HTMLBOOK}

clean:
	rm -rf ${PDFBOOK} ${HTMLBOOK} ${PYTHONFIGS} simbook.Rmd book_output/*

${PDFBOOK}: ${PYTHONFIGS} ${RMDFILES} ${BIBFILES} ${PYLISTINGS}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::pdf_book",clean=T)'

${HTMLBOOK}: ${PYTHONFIGS} ${RMDFILES} ${BIBFILES} ${PYLISTINGS}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::gitbook",clean=T)'

hudson1990.png: ../simbook/coalescent/hudson1990.py chapters/coalescent/figures/h1990.py
	PYTHONPATH=.. python3 chapters/coalescent/figures/h1990.py

migration.png: ../simbook/coalescent/migration.py chapters/coalescent/figures/compare_migration_to_msprime.py
	PYTHONPATH=.. python3 chapters/coalescent/figures/compare_migration_to_msprime.py

msprime_scaling.png: chapters/coalescent/figures/msprime_scaling.py
	PYTHONPATH=.. python3 chapters/coalescent/figures/msprime_scaling.py
