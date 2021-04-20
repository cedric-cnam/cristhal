
######## Paramètres pour requête HAL

# Config par défaut
CODE_CONFIG_DEFAUT='défaut'

# Le service HAL
HAL_SEARCH_URL = "https://api.archives-ouvertes.fr/search/"

# Une limite sur le nombre de publis à chercher...
MAX_ROWS = 1000
# Séparateur de facettes dans HAL
FACET_SEP="_FacetSep_"
JOIN_SEP="_JoinSep_"
# Motif de l'URL de recherche des publis
QUERY_PUBLIS=HAL_SEARCH_URL + "CEDRIC-CNAM?wt=json&fq=publicationDateY_i:[{ymin:d} TO {ymax:d}]&sort=producedDate_tdate%20desc" 
# Recherche d'un auteur par son id HAL
QUERY_AUTEUR="https://api.archives-ouvertes.fr/ref/author/?fq=idHal_s:{id_hal:s}&&fl=firstName_s&fl=lastName_s&fl=structure_fs"
# Recherche d'un auteur par son identifiant interne
QUERY_AUTEUR_ID="https://api.archives-ouvertes.fr/ref/author/?wt=json&q=docid:{id:d}"
# Recherche structure par id interne
QUERY_STRUCTURE="https://api.archives-ouvertes.fr/ref/structure/?wt=json&q=docid:{id:d}"
# Recherche des structures d'un auteur
QUERY_STRUCTURES_AUTEUR="https://api.archives-ouvertes.fr/search/authorstructure/?firstName_t={prenom:s}&lastName_t={nom:s}&getParents=false"
# Requête publis équipe
QUERY_HAL_COLL = HAL_SEARCH_URL + "?wt=json&q=*:*&facet=true&fq=publicationDateY_i:[{ymin:d} TO {ymax:d}]&fq=structId_i:{coll_id:d}"
# Requête pour une publi
QUERY_HAL_PUBLI = HAL_SEARCH_URL + "?wt=bibtex&fq=halId_s:{id_hal:s}"
# Liste des champs à récupérer pour une publi
CHAMPS = ["halId_s",  "journalTitle_s", "title_s", 
        "docType_s", 
        "authIdHalFullName_fs", "authIdFullName_fs",
        "authIdHasStructure_fs",
        "conferenceTitle_s", "bookTitle_s",
         "publicationDateY_i", "publisher_s"]

# Quand on veut traiter toutes les collections
TOUTES_COLLECTIONS='toutes'

# Types de publis dans Hal
PUBLI_CONF = "COMM"
PUBLI_REVUE="ART"
PUBLI_POSTER="POSTER"
PUBLI_DIRECTION_OUVRAGE="DOUV"
PUBLI_CHAPITRE="COUV"
PUBLI_OUVRAGE="OUV"
PUBLI_THESE="THESE"
PUBLI_HDR="HDR"
PUBLI_REPORT="REPORT"
PUBLI_UNDEFINED="UNDEFINED"
PUBLI_OUVRAGE="OUV"
PUBLI_BREVET="PATENT"
PUBLI_AUTRE="OTHER"
PUBLI_TOUS_TYPES="Tous"

TYPES_PUBLI= {
        PUBLI_REVUE: "Articles revue",
        PUBLI_CONF: "Conférence",
        PUBLI_DIRECTION_OUVRAGE: "Direction d'ouvrage",
        PUBLI_CHAPITRE: "Chapitre dans ouvrage",
        PUBLI_OUVRAGE: "Livre",
        PUBLI_POSTER: "Poster",
        PUBLI_THESE: "Thèse",
        PUBLI_HDR: "Habilitation",
        PUBLI_REPORT: "Rapport de recherche",
        PUBLI_BREVET: "Brevet",
}

# Le tableau suivant indique les types de publi que l'on ne souhaite par charger
PUBLIS_HAL_EXCLUES = [PUBLI_THESE, PUBLI_HDR, PUBLI_UNDEFINED, 
                      PUBLI_REPORT, PUBLI_AUTRE]

#
# Sources référentiel
#

SOURCE_CORE="CORE"
SOURCE_SCIMAGO="SCIMAGO"
SOURCE_INTERNE="INTERNE"

# Pour indiquer le type de source dans le formulaire Django
CHOIX_SOURCES = (
    (SOURCE_CORE, "Sources CORE"),
    (SOURCE_SCIMAGO, "Sources SCIMAGO"),
    (SOURCE_INTERNE, "Sources interne"),
)
