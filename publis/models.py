from django.db import models
import requests
import csv 
import logging

from .constants import *
from _collections import OrderedDict

from .IndexWrapper import IndexWrapper

# Un journaliseur 
logger = logging.getLogger("pubrank")



#################
class Config(models.Model):
    """
        Configuration de l'appli
    """
    
    # Période par défaut
    ANNEE_MIN_PUBLI=2017
    ANNEE_MAX_PUBLI=2021
    
    code = models.CharField(max_length=20, default="défaut", primary_key=True)
    
    # URL d'interrogation de Ham
    url_hal = models.CharField(max_length=80, default=HAL_SEARCH_URL)
    annee_min_publis = models.IntegerField(default=ANNEE_MIN_PUBLI)
    annee_max_publis = models.IntegerField(default=ANNEE_MAX_PUBLI)

    class Meta:
        db_table = "Config"

    def __str__(self):              # __unicode__ on Python 2
        return self.code

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

    @staticmethod
    def stats_collections(annee_min, annee_max, type_publi=PUBLI_REVUE):
        # La sortie: un dictionnaire sur le code de la collection, chaque entrée est le nombre de publis
        sortie = []
        for coll in Collection.objects.all():
            # Comptons les publications tu type demandé
            publis = Publication.get_publis_periode (coll.code, 
                                                     annee_min, 
                                                     annee_max, 
                                                     type_publi)
            sortie.append ({"name": coll.code, "y": publis.count()})
            
        return sortie

#################
class Collection(models.Model):
    """
        Paramétrage d'une collection Hal
    """
    
    code = models.CharField(max_length=20, unique=True)
    # Le nom de la collection dans Hal. P.e. 'CEDRIC-VERTIGO'
    sigle_hal = models.CharField(max_length=40, unique=True)
    # Identifiant le la collection Hal (un chiffre)
    id_hal = models.IntegerField(unique=True,null=True)
    # Le nom local, à utiliser pour les affichages
    nom = models.CharField(max_length=80, default="À définir")
    description = models.TextField()
    email_contact = models.CharField(max_length=40)
    
    class Meta:
        db_table = "Collection"

    def __str__(self):              # __unicode__ on Python 2
        return self.nom + " (" + self.code + ")"

    def __init__(self, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)

    def synchro_hal(self):
        
        # Cherchons la configuration pour avoir des valeurs par défaut
        config = Config.objects.get(code=CODE_CONFIG_DEFAUT)

        # On crée l'URL d'interrogation de HAL
        #"Sammy the {pr} {1} a {0}.".format("shark", "made", pr = "pull request"))
        hal_query = QUERY_HAL_COLL.format(coll_id=self.id_hal,
                                        ymin=config.annee_min_publis, 
                                        ymax=config.annee_max_publis)
        for c in CHAMPS:
            hal_query += "&fl=" + c
        hal_query += "&rows=" + str(MAX_ROWS)
        
        # On récupère toutes les publis de Hal pour synchroniser la base
        logger.info("Requête HAL : " + hal_query)
        i_doc = 0
        r = requests.get(url=hal_query)
        docs = r.json()["response"]["docs"]
        for doc in docs: 
            if not (doc["docType_s"] in PUBLIS_HAL_EXCLUES):
                # Si elle existe, on la garde avec son classement
                try:
                    publi = Publication.objects.get(idHal=doc["halId_s"])
                    #print ("Modification de la publi " + publi.idHal)
                except Publication.DoesNotExist:
                    publi = Publication(idHal=doc["halId_s"])
                    #print ("Création de la publi " + publi.idHal)
                # On modifie d'après le JSON
                publi.fromJson(doc)
                publi.save()
                # On ajoute la collection
                publi.collections.add(self)
                publi.save()
                i_doc += 1

        logger.info("{0} publications ont été chargées depuis HAL dans la collection {1}".format(
            str(i_doc), self.code))
        return i_doc

    def nb_publis(self):
        return self.publication_set.count()

#################
class Source(models.Model):
    """ 
        Infos sur un fichier CSV à charger dans le référentiel
    """

    fichier = models.FileField()
    description = models.CharField(max_length=255)
    # Préfixe unique à ajouter à l'identifiant pour pouvoir retrouver la ref ensuite
    identifiant_source = models.CharField(max_length=30,unique=True)
    # Délimiteur CSV
    delimiteur =  models.CharField(max_length=5,default=';')
    # Type de source (le format change légèrement)
    type_source = models.CharField(
        max_length=30,
        choices=CHOIX_SOURCES,
        default=SOURCE_CORE,
    )
    class Meta:
        db_table = "Source"

    def __str__(self):              # __unicode__ on Python 2
        return self.description + " (identifiant: %s)" % self.identifiant_source

    def __init__(self, *args, **kwargs):
        super(Source, self).__init__(*args, **kwargs)

    def count_refs (self):
        return Referentiel.objects.filter(source=self).count()

    def chargement_fichier(self):
        """
          Important: chaque fichier CSV doit comprendre une première ligne indiquand
            l'emplacement des colonnes ID,  Titre et Classement. On peut aussi trouver Acronyme et Type
        
            Il faut ajouter cette ligne pour les fichierss CORE. 
              Pour les confs: ID,Titre,Acronyme,source,Classement,dblp,hasData,domaine,commentaires,notes
              Pour les revues: ID,titre,source,classement,dblp,hasData,domaine,domaine2,domaine3
          
            Il faut renommer certains champs pour les fichiers SCIMAGO
        
             Pour les fichiers internes, la première ligne doit indiquer les colonnes ID, Titre, classement
         
            Pour les fichiers CORE le type n'existe pas: il est passé en paramètre
            L'acronyme n'existe pas dans les fichiers SCIMAGO
        """

        logger.info("Chargement du fichier source {0}".format(self.description))
        
        # Supprimons les refs Elastic Search
        es_index = IndexWrapper()
        for ref in Referentiel.objects.filter(source=self):
            es_index.delete_ref(ref)

        # Supprimons toutes les références de la base de données
        Referentiel.objects.filter(source=self).delete()

        nb_refs = 0
        with open(self.fichier.path,'r',  encoding="utf8" ) as fichier_source:
            reader = csv.DictReader(fichier_source,  delimiter=self.delimiteur)
            for row in reader:
            
                # Attention on ne prend pas les conférences dans SCIMAGO
                if self.type_source == SOURCE_SCIMAGO and not (
                     row['Type'] == "journal"):
                    continue
            
                nb_refs += 1
                # La ref locale permet de s'assurer qu'il n'y a pas de collisioo
                ref_locale = self.identifiant_source + ":" + row['ID']
                try:
                    ref = Referentiel.objects.get(ref_locale=ref_locale)
                    # Remplacement de la référence 
                    ref.delete()
                except Referentiel.DoesNotExist:
                    pass
            
                if "Acronyme" in row.keys():
                    acronyme = row['Acronyme']
                else:
                    acronyme = ""
                
                if self.type_source == SOURCE_INTERNE:
                    # Le type doit être "ART" ou "COMM"
                    type_ref = row["Type"]
                elif self.type_source == SOURCE_SCIMAGO:
                    # Le type est 'journal' ou 'conf'
                    if row['Type'] == 'journal':
                        type_ref = PUBLI_REVUE
                    else:
                        type_ref = PUBLI_CONF
                else:
                    # pour CORE on bricole un peu ...
                    if "core_confs" in self.identifiant_source:
                        type_ref = PUBLI_CONF
                    else:
                        type_ref = PUBLI_REVUE
 
                ref = Referentiel (source=self, 
                                   ref_locale=ref_locale,type=type_ref, 
                                   acronyme=acronyme,titre=row["Titre"],
                                   champ_plein_texte=(row["Titre"] + " " +  acronyme).lower(),
                                   classement=row["Classement"])
                ref.save()

        # Indexation ElasticSearch
        for ref in Referentiel.objects.filter(source=self):
            es_index.store_ref(ref)

        logger.info("{0} références ont été chargées".format(str(nb_refs)))

        return nb_refs

#################
class Referentiel(models.Model):
    """ 
        Référentiel des revues et conférences
    """

    source = models.ForeignKey(Source,on_delete=models.PROTECT,null=True)
    ref_locale = models.CharField(max_length=40,null=True)
    type = models.CharField(max_length=10,default='COMM')
    acronyme = models.CharField(max_length=80)
    titre = models.TextField()
    champ_plein_texte = models.TextField(default='')
    classement = models.CharField(max_length=30)
    
    class Meta:
        db_table = "Referentiel"

    def __str__(self):              # __unicode__ on Python 2
        return self.titre + " (" + self.acronyme + ")"

    def __init__(self, *args, **kwargs):
        super(Referentiel, self).__init__(*args, **kwargs)


#################
class Auteur(models.Model):

    """
       Une table pour collecter les auteurs et co-auteurs
    """
    
    # 
    nom_complet = models.CharField(max_length=255)
    # On essaie de récupérer l'id HAL quand il existe
    id_hal = models.CharField(max_length=40,unique=True, null=True)
    
    class Meta:
        db_table = "Auteur"

    def __str__(self):              # __unicode__ on Python 2
        return self.nom_complet

    def __init__(self, *args, **kwargs):
        super(Auteur, self).__init__(*args, **kwargs)


#################
class ClassementPubli(models.Model):

    """
       Les catégories de classement
    """
    
    code = models.CharField(max_length=4, primary_key=True)
    libelle = models.CharField(max_length=255,)
    
    class Meta:
        db_table = "ClassementPubli"

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % (self.libelle)

    def __init__(self, *args, **kwargs):
        super(ClassementPubli, self).__init__(*args, **kwargs)

#################
class Publication(models.Model):

    """
       Les publications importées de Hal
    """
    
    idHal = models.CharField(max_length=100, primary_key=True)
    titre = models.CharField(max_length=255)
    annee = models.IntegerField()
    type = models.CharField(max_length=30)
    # Une publication peut être dans plusieurs collections
    collections = models.ManyToManyField(Collection, blank=True)
    # On enregistre les auteurs
    auteurs = models.ManyToManyField(Auteur, blank=True)
    # Une chaîne avec le nom des auteurs pour la recherche
    chaine_auteurs = models.TextField(blank=True, null=True)
    revue_titre = models.CharField(max_length=255, blank=True, null=True)
    conf_titre = models.CharField(max_length=255, blank=True, null=True)
    ouvrage_titre = models.CharField(max_length=255, blank=True, null=True)
    
    # Classement des publis + indicateur si le classement a été validé
    classement =  models.ForeignKey(ClassementPubli,default='I',on_delete=models.PROTECT)
    classement_valide = models.BooleanField(default=False)

    class Meta:
        db_table = "Publi"

    def __str__(self):              # __unicode__ on Python 2
        return self.titre

    def __init__(self, *args, **kwargs):
        super(Publication, self).__init__(*args, **kwargs)

    @staticmethod
    def stats_par_annee_type(collection, annee_min, annee_max):
        publis = Publication.get_publis_periode (collection, annee_min, annee_max)                        
        # La sortie: un dictionnaire sur le type, chaque entree est un tableau avec le compte par année
        sortie = OrderedDict()
        for type_publi, libelle_publi in TYPES_PUBLI.items():
            sortie[libelle_publi] = list()
            for annee in range (annee_min, annee_max+1):
                nb_par_annee = 0
                # On trouve dans le résultat de la requete les publis pour cette annee et ce type                
                for publi in publis:
                    if publi.type == type_publi and publi.annee==annee:
                        nb_par_annee += 1
                sortie[libelle_publi].append(nb_par_annee)
        return sortie

    @staticmethod
    def stats_par_annee_classement(collection, annee_min, annee_max):
        publis = Publication.get_publis_periode (collection, annee_min, annee_max)                        
        # La sortie: un dictionnaire sur le type, chaque entree est un tableau avec le compte par année
        sortie = OrderedDict()
        for classement in ClassementPubli.objects.all():
            sortie[classement.libelle] = list()
            for annee in range (annee_min, annee_max+1):
                nb_par_annee = 0
                # On trouve dans le résultat de la requete les publis pour cette annee et ce classement                
                for publi in publis:
                    if publi.classement_valide and publi.classement == classement and publi.annee==annee:
                        nb_par_annee += 1
                sortie[classement.libelle].append(nb_par_annee)
        return sortie

    @staticmethod
    def stats_par_classement(collection, annee_min, annee_max):
        # On exclut le niveau Comm et le niveau Nat. À paramétrer
        NIVEAUX_EXCLUS = ["C", "N"]
        # La sortie: un dictionnaire sur le type, chaque entree est un tableau avec le compte par année
        classements = ClassementPubli.objects.all()
        sortie = []
        for classement in classements:
            # Pour cette stat on ne prend pas les comm
            if not (classement.code in NIVEAUX_EXCLUS):
                sortie.append ({"name": classement.libelle, "y":0, "type": classement.code })
        for publi in Publication.get_publis_periode (collection, annee_min, annee_max):
            if publi.classement_valide and not (publi.classement.code in NIVEAUX_EXCLUS):
                for count_type in sortie:
                    if count_type["type"] ==  publi.classement.code:
                        count_type["y"] +=  1
        return sortie

    @staticmethod
    def get_publis_periode (collection_code, annee_min, annee_max, type_publi=PUBLI_TOUS_TYPES):
               
        # La requete : toutes les publis de la période
        if collection_code == TOUTES_COLLECTIONS:
            publis =  Publication.objects.filter(
                        annee__gte=annee_min).filter(
                        annee__lte=annee_max)
        else:
            publis =   Publication.objects.filter(
                        annee__gte=annee_min).filter(
                        annee__lte=annee_max).filter(
                        collections__code=collection_code)
        
        if not (type_publi == PUBLI_TOUS_TYPES):
            # Filtre supplémentaire sur le type
            publis = publis.filter(type=type_publi)
            
        return publis

    def fromJson(self, jsonDoc):
        """
            Exctraction des données d'une publication du JSON renvoyé par Hal
        """
        self.titre = jsonDoc["title_s"][0]
        self.annee = jsonDoc["publicationDateY_i"]
        self.type = jsonDoc["docType_s"]
        if self.type == PUBLI_REVUE:
            self.revue_titre = jsonDoc["journalTitle_s"]
        elif self.type == PUBLI_CONF:
            self.conf_titre = jsonDoc["conferenceTitle_s"]
        elif self.type == PUBLI_CHAPITRE:
            self.ouvrage_titre = jsonDoc["title_s"]
        elif self.type == PUBLI_OUVRAGE or self.type == PUBLI_DIRECTION_OUVRAGE:
            self.ouvrage_titre = jsonDoc["title_s"]
        self.save()
        
        if "authIdHalFullName_fs" in jsonDoc.keys():
            chaine_auteurs = ""
            for auteur in jsonDoc["authIdHalFullName_fs"]:
                comps = auteur.split(FACET_SEP)
                # Premier compoosant: idHal, second: nom complet
                try:
                    auteur = Auteur.objects.get(nom_complet=comps[1])
                except Auteur.DoesNotExist:
                    auteur = Auteur(nom_complet=comps[1])
                    #Peut-être on a l'id HAL
                    if comps[0] != '':
                        auteur.id_hal = comps[0]
                    auteur.save()
                chaine_auteurs +=  comps[1] + ' '      
                
            self.chaine_auteurs = chaine_auteurs
            self.auteurs.add(auteur)
            self.save()
