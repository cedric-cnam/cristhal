# On peut produire les formats graphiques
# avec les outils Highcharts (https://www.highcharts.com/docs/export-module).
# Il faut essentiellement installer le *Highcharts export server*, en fait 
# un utilitaire Javascript, selon les instructions qui se trouvent
# sur la page Github https://github.com/highcharts/node-export-server/blob/master/README.md.


INPUTS := $(wildcard ./stats_publis/*.json)

# Liste des fichiers à engendrer
OUTPUTS := $(patsubst ./stats_publis/%.json,./stats_publis/%.pdf,$(INPUTS))

# Par défaut on compile tous les PDF
all: $(OUTPUTS)

biblio:
	pdflatex biblio_{equipe}.tex
	make clean
	
%.pdf: %.json
	highcharts-export-server -type pdf -infile $*.json -outfile $*.pdf

clean:
	/bin/rm -f ./stats_publis/*.pdf
	/bin/rm -f *.dvi *.toc *.ps *.log *.aux *.mtc* *.tar *.gz *.maf *.idx *.out *.bcf 
