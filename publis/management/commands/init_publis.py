from django.core.management.base import BaseCommand

from publis.models import ClassementPubli, Config

from publis.constants import HAL_SEARCH_URL, CODE_CONFIG_DEFAUT

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
        for cl in CLASSEMENT_PUBLIS:
            try:
                class_obj = ClassementPubli.objects.get(code=cl["code"])
                print ("Le classement " + cl["libelle"] + " existe déjà")
            except ClassementPubli.DoesNotExist:
                print ("Création du classement  ({0}, {1})".format (
                    cl["code"], cl["libelle"]))
                class_obj = ClassementPubli(code=cl["code"],libelle=cl["libelle"])
                class_obj.save()
        print ("Classement des publis initialisé")
