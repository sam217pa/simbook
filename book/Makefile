PDFBOOK:=book_output/simbook.pdf
HTMLBOOK:=book_output/coalescent-simulation.html

RMDFILES:=index.Rmd chapters/coalescent.Rmd chapters/references.Rmd 
BIBFILES:=chapters/simbook.bib
PYTHONFIGS=hudson1990.png migration.png

all: ${PDFBOOK} ${HTMLBOOK}

clean:
	rm -rf ${PDFBOOK} ${HTMLBOOK} ${PYTHONFIGS} simbook.Rmd book_output/*

${PDFBOOK}: ${PYTHONFIGS} ${RMDFILES} ${BIBFILES}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::pdf_book",clean=T)'

${HTMLBOOK}: ${PYTHONFIGS} ${RMDFILES} ${BIBFILES}
	RETICULATE_PYTHON=`which python3` PYTHONPATH=.. r -e 'bookdown::render_book("index.Rmd","bookdown::gitbook")'

hudson1990.png: ../simbook/coalescent/hudson1990.py figures/python/h1990.py
	PYTHONPATH=.. python3 figures/python/h1990.py

migration.png: ../simbook/coalescent/migration.py figures/python/compare_migration_to_msprime.py
	PYTHONPATH=.. python3 figures/python/compare_migration_to_msprime.py
