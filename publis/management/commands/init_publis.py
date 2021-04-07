from django.core.management.base import BaseCommand

from publis.models import ClassementPubli, Config

from publis.constants import CLASSEMENT_PUBLIS, HAL_SEARCH_URL, CODE_CONFIG_DEFAUT

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
