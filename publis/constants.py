
######## Paramètres pour requête HAL

# Config par défaut
CODE_CONFIG_DEFAUT='défaut'
ANNEE_MIN_PUBLI=2017
ANNEE_MAX_PUBLI=2021
# Le service HAL
HAL_SEARCH_URL = "https://api.archives-ouvertes.fr/search/"

# Une limite sur le nombre de publis à chercher...
MAX_ROWS = 1000
# Motif de l'URL de recherche des publis
QUERY_PUBLIS=HAL_SEARCH_URL + "CEDRIC-CNAM?wt=json&fq=publicationDateY_i:[{ymin:d} TO {ymax:d}]&sort=producedDate_tdate%20desc" 

# Liste des champs à récupérer
CHAMPS = ["halId_s",  "journalTitle_s", "title_s", 
        "docType_s", 
        "authIdHalFullName_fs", 
        "conferenceTitle_s", "bookTitle_s",
         "publicationDateY_i", "publisher_s", "rteamStructAcronym_s"]

# Séparateur de facettes dans HAL
FACET_SEP="_FacetSep_"
# Requête publis équipe
QUERY_HAL_COLL = HAL_SEARCH_URL + "?wt=json&q=*:*&facet=true&fq=publicationDateY_i:[{ymin:d} TO {ymax:d}]&fq=structId_i:{coll_id:d}"

# Code des équipes dans HAL
HAL_EQUIPES= {
        "cedric": 16574,
        "vertigo": 553459,
        "isid":  392824,
        "sys": 553461,
        "ilj": 573796,
        "oc": 553460,
        "roc": 552483,
        "msdma": 390785,
        "laetitia": 393635
}

# Quand on veut traiter toutes les collections
TOUTES_COLLECTIONS='toutes'

# Types de publis dans Hal
PUBLI_CONF = "COMM"
PUBLI_REVUE="ART"
PUBLI_DIRECTION_OUVRAGE="DOUV"
PUBLI_CHAPITRE="COUV"
PUBLI_OUVRAGE="OUV"
PUBLI_THESE="THESE"
PUBLI_HDR="HDR"
PUBLI_REPORT="REPORT"
PUBLI_UNDEFINED="UNDEFINED"
PUBLI_OUVRAGE="OUV"
PUBLI_AUTRE="OTHER"

TYPES_PUBLI= {
        PUBLI_REVUE: "Articles revue",
        PUBLI_CONF: "Conférence",
        PUBLI_DIRECTION_OUVRAGE: "Direction d'ouvrage",
        PUBLI_CHAPITRE: "Chapitre dans ouvrage",
        PUBLI_OUVRAGE: "Livre",
}

# Le tableau suivant indique les types de publi que l'on ne souhaite par charger
PUBLIS_HAL_EXCLUES = [PUBLI_THESE, PUBLI_HDR, PUBLI_UNDEFINED, 
                      PUBLI_REPORT, PUBLI_AUTRE]

# Codes pour le classement
NIVEAU_1 = "N1"
NIVEAU_2 = "N2"
NIVEAU_3 = "N3"
NIVEAU_4 = "N4"
NIVEAU_COMM = "C"
NIVEAU_NAT = "N"
NIVEAU_HORS_REFERENTIEL = "I"
CLASSEMENT_PUBLIS = [{"code": NIVEAU_1, "libelle" : "Q1"},
                     {"code": NIVEAU_2, "libelle" : "Q2"},
                     {"code": NIVEAU_3, "libelle" : "Q3"},
                     {"code": NIVEAU_4, "libelle" : "Q4"},
                   {"code": NIVEAU_COMM, "libelle" : "Communications"},
                    {"code": NIVEAU_NAT, "libelle" : "National"},
                    {"code": NIVEAU_HORS_REFERENTIEL, "libelle" : "Hors référentiel"}
]

#
# Sources référentiel
#

SOURCE_CORE="CORE"
SOURCE_SCIMAGO="SCIMAGO"
SOURCE_INTERNE="INTERNE"

# Pour indiquer le type de source dans le formulaire Django
CHOIX_SOURCES = (
    (SOURCE_CORE, "Fichier d'import CORE"),
    (SOURCE_SCIMAGO, "Fichier d'import SCIMAGO"),
    (SOURCE_INTERNE, "Fichier d'import format interne"),
)