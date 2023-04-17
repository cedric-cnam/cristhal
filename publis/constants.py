
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
QUERY_AUTEUR_ID="https://api.archives-ouvertes.fr/ref/author/?wt=json&fq=idHal_i:{id_hal}&fl=firstName_s&fl=lastName_s&fl=idHal_s"
# Recherche structure par id interne
QUERY_STRUCTURE="https://api.archives-ouvertes.fr/ref/structure/?wt=json&q=docid:{id:d}"
# Recherche des structures d'un auteur
QUERY_STRUCTURES_AUTEUR="https://api.archives-ouvertes.fr/search/authorstructure/?firstName_t={prenom:s}&lastName_t={nom:s}&getParents=false"
# Requête publis équipe
QUERY_HAL_COLL = HAL_SEARCH_URL + "?wt=json&q=*:*&facet=true&fq=publicationDateY_i:[{ymin:d} TO {ymax:d}]&fq=structId_i:{coll_id:d}"
# Requête pour une publi
QUERY_HAL_PUBLI = HAL_SEARCH_URL + "?wt=bibtex&fq=halId_s:{id_hal:s}"
# Liste des champs à récupérer pour une publi
CHAMPS = ["halId_s",  "title_s", "label_bibtex,"
        "docType_s", "authIdHasStructure_fs",
        "conferenceTitle_s", 
         "publicationDateY_i", "bookTitle_s", "publisher_s",  "number_s", "page_s", "volume_s",
         "journalTitle_s","journalPublisher_s"]

# "authIdHalFullName_fs", "authIdFullName_fs",

# Quand on veut traiter toutes les collections
TOUTES_COLLECTIONS='toutes'

# Types de publis dans Hal
PUBLI_CONF = "COMM"
PUBLI_REVUE="ART"
PUBLI_POSTER="POSTER"
PUBLI_DIRECTION_OUVRAGE="DOUV"
PUBLI_ACTES="PROCEEDINGS"
PUBLI_CHAPITRE="COUV"
PUBLI_OUVRAGE="OUV"
PUBLI_THESE="THESE"
PUBLI_HDR="HDR"
PUBLI_REPORT="REPORT"
PUBLI_UNDEFINED="UNDEFINED"
PUBLI_BREVET="PATENT"
PUBLI_LOGICIEL="SOFTWARE"
PUBLI_AUTRE="OTHER"
PUBLI_TOUS_TYPES="Tous"
PUBLI_TOUS_CLASSEMENTS="Tous"

# Un dictionnairee avec les types de publi
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
        PUBLI_AUTRE: "Autre",
        PUBLI_LOGICIEL: "Logiciel"
}

# Les types suivants sont classés en Communication
TYPES_PUBLI_COMMUNICATION = [PUBLI_POSTER, PUBLI_DIRECTION_OUVRAGE, PUBLI_ACTES,
					PUBLI_CHAPITRE, PUBLI_OUVRAGE, PUBLI_REPORT]

# Les types suivants sont classés en Valorisation
TYPES_PUBLI_VALORISATION = [PUBLI_BREVET, PUBLI_LOGICIEL]

# Les types de publi que l'on ne souhaite par charger
#  par défaut
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


# Les valeurs du classement par défaut

NIVEAU_1 = "N1"
NIVEAU_2 = "N2"
NIVEAU_3 = "N3"
NIVEAU_4 = "N4"
NIVEAU_COMM = "C"
NIVEAU_NAT = "N"
NIVEAU_VALO = "V"
NIVEAU_HORS_REF = "I"
CLASSEMENT_PUBLIS = [{"code": NIVEAU_1, "libelle" : "Q1"},
                     {"code": NIVEAU_2, "libelle" : "Q2"},
                     {"code": NIVEAU_3, "libelle" : "Q3"},
                     {"code": NIVEAU_4, "libelle" : "Q4"},
                   {"code": NIVEAU_COMM, "libelle" : "Communications"},
				   {"code": NIVEAU_VALO, "libelle" : "Valorisation"},
                    {"code": NIVEAU_NAT, "libelle" : "National"},
                    {"code": NIVEAU_HORS_REF, "libelle" : "Hors référentiel"}
                ]
