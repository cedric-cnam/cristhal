#
# Exemple de fichier Make pour produire les image sà partir des JSON exportés de CristHAL
#
# Utilise Highcharts "node export server" pour produire les images à partir
# des JSON. Attention pour l'installation à préciser l'option suivante:
#
#  --unsafe-perm
#


# On traite les json
INPUTS := $(wildcard ./*.json)
# Tous les fichiers que nous voulons engendrer
OUTPUTS := $(patsubst ./%.json,./%.pdf,$(INPUTS))

# Par défaut on produit tout
all: $(OUTPUTS)


%.pdf: %.json
	highcharts-export-server -type pdf -infile $*.json -outfile $*.pdf

clean:
	rm -f *.pdf
