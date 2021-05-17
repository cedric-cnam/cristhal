from django.core.management.base import BaseCommand

from publis.models import ClassementPubli, Config, TypesHAL

from publis.constants import *

# Les valeurs du classement par défaut

NIVEAU_1 = "N1"
NIVEAU_2 = "N2"
NIVEAU_3 = "N3"
NIVEAU_4 = "N4"
NIVEAU_COMM = "C"
NIVEAU_NAT = "N"
NIVEAU_HORS_REF = "I"
CLASSEMENT_PUBLIS = [{"code": NIVEAU_1, "libelle" : "Q1"},
                     {"code": NIVEAU_2, "libelle" : "Q2"},
                     {"code": NIVEAU_3, "libelle" : "Q3"},
                     {"code": NIVEAU_4, "libelle" : "Q4"},
                   {"code": NIVEAU_COMM, "libelle" : "Communications"},
                    {"code": NIVEAU_NAT, "libelle" : "National"},
                    {"code": NIVEAU_HORS_REF, "libelle" : "Hors référentiel"}
                ]


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
}

# Le tableau suivant indique les types de publi que l'on ne souhaite par charger
#  par défaut
PUBLIS_HAL_EXCLUES = [PUBLI_THESE, PUBLI_HDR, PUBLI_UNDEFINED, 
                      PUBLI_REPORT, PUBLI_AUTRE]


class Command(BaseCommand):
    """Initialisation de la codification """

    help = 'Create some mandatory objects in the DB'
    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        # Création de la config par défaut
        try:
            conf_def = Config.objects.get(code=CODE_CONFIG_DEFAUT)
        except Config.DoesNotExist:
            print ("Création de la configuration par défaut")
            conf_def =  Config (code=CODE_CONFIG_DEFAUT, url_hal=HAL_SEARCH_URL)
            conf_def.save()

        # Initialisation de l'échelle des classement
        print ("Initialisation de l'échelle de classement des publications")
        for cl in CLASSEMENT_PUBLIS:
            try:
                class_obj = ClassementPubli.objects.get(code=cl["code"])
                print ("\tLe classement " + cl["libelle"] + " existe déjà")
            except ClassementPubli.DoesNotExist:
                print ("Création du classement  ({0}, {1})".format (
                    cl["code"], cl["libelle"]))
                class_obj = ClassementPubli(code=cl["code"],libelle=cl["libelle"])
                class_obj.save()

        # Insertion des types de publication HAL
        print ("Initialisation des types de publication HAL")
        for code, libelle in TYPES_PUBLI.items():
            try:
                thal_obj = TypesHAL.objects.get(code=code)
                print ("\tLe type " + code + " existe déjà")
            except TypesHAL.DoesNotExist:
                print ("Création du type de publi  ({0}, {1})".format (
                    code, libelle))
                thal_obj = TypesHAL(code=code,libelle=libelle)
                thal_obj.save()
                if not code in PUBLIS_HAL_EXCLUES:
                    conf_def.types_publis.add(thal_obj)
                    
        print ("\nInitialisation terminée")
