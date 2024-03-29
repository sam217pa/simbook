PDFBOOK:=book_output/simbook.pdf
HTMLBOOK:=book_output/coalescent-simulation.html

RMDFILES:=index.Rmd $(shell find chapters -type f -name '*.Rmd')
RMDFILES+=$(shell find appendix -type f -name '*.Rmd')
BIBFILES:=chapters/simbook.bib
PYLISTINGS:=$(shell find chapters -type f -name '*.py' | grep listings)
PYTHONPACKAGE:=$(shell find ../simbook -type f -name '*.py' | grep -v __init__)
PYTHONFIGS=hudson1990.png migration.png msprime_scaling.png \
		   drawtree.png tskittree.png \
		   twotrees.png smalltree.png \
		   nonbifurcating.png \
		   splitscaling.png

# Cheat sheet: https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

all: ${PDFBOOK} ${HTMLBOOK}

clean:
	rm -rf ${PDFBOOK} ${HTMLBOOK} ${PYTHONFIGS} simbook.Rmd book_output/* *.svg *.png *.o

${PDFBOOK}: ${PYTHONFIGS} ${RMDFILES} ${BIBFILES} ${PYLISTINGS}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::pdf_book",clean=T)'

# NOTE: the html output depends on the pdf being built
# because we have some hacky things involving msprime's DemographyDebugger,
# and I worry about overwriting files if the two render steps executed at the
# same time via a "make -j x" command.
${HTMLBOOK}: ${PDFBOOK} ${PYTHONFIGS} ${RMDFILES} ${BIBFILES} ${PYLISTINGS}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::gitbook",clean=T)'

# Figure are starting here

# Tree sequences

drawtree.svg: chapters/treeseqs/figures/drawtree.py
	python3 $?

drawtree.png: drawtree.svg
	convert -density 300  $? $@

tskittree.svg: chapters/treeseqs/figures/tskittree.py
	python3 $?

tskittree.png: tskittree.svg
	convert -density 300 $? $@

twotrees1.svg: chapters/treeseqs/figures/twotrees.py
	python3 $?

twotrees1.png: twotrees1.svg
	convert -density 300 $? $@

twotrees0.svg: chapters/treeseqs/figures/twotrees.py
	python3 $?

twotrees0.png: twotrees0.svg
	convert -density 300 $? $@

twotrees.png: twotrees0.png twotrees1.png
	convert +append $^ $@

smalltree.svg: chapters/treeseqs/figures/smalltree.py
	python3 $?

smalltree.png: smalltree.svg
	convert -density 300 $? $@

nonbifurcating.svg: chapters/treeseqs/figures/nonbifurcating.py
	python3 $?

nonbifurcating.png: nonbifurcating.svg
	convert -density 300 $? $@

# Coalescent

hudson1990.png: ../simbook/coalescent/hudson1990.py chapters/coalescent/figures/h1990.py
	PYTHONPATH=.. python3 chapters/coalescent/figures/h1990.py

migration.png: ../simbook/coalescent/migration.py chapters/coalescent/figures/compare_migration_to_msprime.py
	PYTHONPATH=.. python3 chapters/coalescent/figures/compare_migration_to_msprime.py

# Simulation using msprime

msprime_scaling.png: chapters/msprime/figures/msprime_scaling.py
	PYTHONPATH=.. python3 chapters/msprime/figures/msprime_scaling.py

splitscaling.png: chapters/msprime/figures/split_and_Ne.py
	python3 $?
