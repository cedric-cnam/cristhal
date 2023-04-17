from django.core.management.base import BaseCommand

from publis.models import ClassementPubli, Config, TypesHAL

from publis.constants import *




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
