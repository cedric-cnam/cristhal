
import requests
import csv 
import logging
import datetime
import os
import shutil
import io


from django.db import models
from django.db.models import Sum, Count
from django.conf import settings

from django.template.response import SimpleTemplateResponse

from .constants import *
from _collections import OrderedDict

import publis.constants as publi_constants

from .IndexWrapper import IndexWrapper

# Un journaliseur 
logger = logging.getLogger(settings.LOGGER_NAME)


#################
class TypesHAL(models.Model):

	"""
	   Les types de publication HAL
	"""
	
	code = models.CharField(max_length=20, primary_key=True)
	libelle = models.CharField(max_length=255,)
	
	class Meta:
		db_table = "TypesHAL"

	def __str__(self):			  # __unicode__ on Python 2
		return "%s" % (self.libelle)

#################
class Config(models.Model):
	"""
		Configuration de l'appli
	"""
	
	# Période par défaut
	ANNEE_MIN_PUBLI=2017
	ANNEE_MAX_PUBLI=2021
	
	code = models.CharField(max_length=20, default="défaut", primary_key=True)
	
	# URL d'interrogation de Hal
	url_hal = models.CharField(max_length=80, default=HAL_SEARCH_URL)
	annee_min_publis = models.IntegerField(default=ANNEE_MIN_PUBLI)
	annee_max_publis = models.IntegerField(default=ANNEE_MAX_PUBLI)

	# Les types de publi HAL à charger
	types_publis = models.ManyToManyField(TypesHAL)

	# Chemin vers le répertoire d'export
	repertoire_export = models.CharField(max_length=100, default="/tmp")

	class Meta:
		db_table = "Config"

	def __str__(self):			  # __unicode__ on Python 2
		return self.code

	def __init__(self, *args, **kwargs):
		super(Config, self).__init__(*args, **kwargs)

	def types_publis_acceptes(self):
		resultat = []
		# Tableau de la liste des types de publis gérés dans HAL
		for type_publi in self.types_publis.all():
			resultat.append(type_publi.code)
		return resultat

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

	@staticmethod
	def stats_types_publis():
		# La sortie: un dictionnaire sur le type de publi, chaque entrée est le nombre de publis par type
		group_type = Publication.objects.values('type').annotate(Count('id_hal'))
		sortie = []
		for gr in group_type:
			type_publi = TypesHAL.objects.get(code=gr["type"])
			sortie.append ({"name": type_publi.libelle, "y": gr["id_hal__count"]})
		return sortie

#################
class Auteur(models.Model):

	"""
	   Une table pour collecter les auteurs et co-auteurs
	"""
	
	# Etrangement on peut avoir deux auteurs avec le même identifiant interne, ex 180351 M. Crucianu
	id_interne = models.IntegerField(null=True)
	prenom = models.CharField(max_length=255,null=True)
	nom = models.CharField(max_length=255,null=True)
	nom_complet = models.CharField(max_length=255)
	# On essaie de récupérer l'id HAL quand il existe
	id_hal = models.CharField(max_length=40,null=True)
	
	class Meta:
		db_table = "Auteur"

	def __str__(self):			  # __unicode__ on Python 2
		return self.nom_complet

	def __init__(self, *args, **kwargs):
		super(Auteur, self).__init__(*args, **kwargs)

	def synchro_hal(self):
		
		# Cherchons la configuration pour avoir des valeurs par défaut
		config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
		types_publis_acceptes = config.types_publis_acceptes()
		
		# On crée l'URL d'interrogation de HAL
		#"Sammy the {pr} {1} a {0}.".format("shark", "made", pr = "pull request"))
		hal_query = QUERY_AUTEUR_ID.format(id_hal=self.id_interne)
		logger.info("Requête HAL Auteur : " + hal_query)
		#print("Requête HAL auteur: " + hal_query)
		i_doc = 0
		r = requests.get(url=hal_query)
		docs = r.json()["response"]["docs"]
		
		if r.json()["response"]["numFound"] == 0:
			logger.info("Auteur inconnu ? : " + hal_query)
			return
		
		self.nom = docs[0]["lastName_s"]
		self.prenom = docs[0]["firstName_s"]
		self.id_hal = docs[0]["idHal_s"]
		#print (f"Prenom {self.prenom} nom {self.nom} id HAL {self.id_hal}")
#
# Participation des auteurs aux collections
#
class Participation(models.Model):
	auteur = models.ForeignKey('Auteur', related_name='participation',on_delete=models.CASCADE)
	collection = models.ForeignKey('Collection', related_name='participation',on_delete=models.CASCADE)
	# On prévoir d'enregistrer la période de participation
	date_debut = models.DateField()
	date_fin = models.DateField()

	class Meta:
		db_table = "Participation"
		constraints = [
			models.UniqueConstraint(fields=['auteur','collection'],
									name='UnicitéAuteurCollection'),
		]
	def __str__(self):
		return self.auteur

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
	# Les auteurs qui on publié pour la collection
	auteurs = models.ManyToManyField(Auteur,
									 related_name='collections',
									 through='Participation',
									 blank=True
									 )
	email_contact = models.CharField(max_length=40)
	
	class Meta:
		db_table = "Collection"

	def __str__(self):
		# __unicode__ on Python 2
		return self.nom + " (" + self.code + ")"

	def __init__(self, *args, **kwargs):
		super(Collection, self).__init__(*args, **kwargs)


	def synchro_hal(self):
		
		# Cherchons la configuration pour avoir des valeurs par défaut
		config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
		types_publis_acceptes = config.types_publis_acceptes()
		
		# On crée l'URL d'interrogation de HAL
		#"Sammy the {pr} {1} a {0}.".format("shark", "made", pr = "pull request"))
		hal_query = QUERY_HAL_COLL.format(coll_id=self.id_hal,
										ymin=config.annee_min_publis, 
										ymax=config.annee_max_publis)
		for c in CHAMPS:
			hal_query += "&fl=" + c
		hal_query += "&rows=" + str(MAX_ROWS)
		
		# Nettoyage de la participation des auteurs à la collection
		Participation.objects.filter(collection=self).delete()
		# On nettoie aussi l'association des publis à la collection: certaine
		# on pu en être retirées
		self.publication_set.clear()
		
		# On récupère toutes les publis de Hal pour synchroniser la base
		logger.info("Requête HAL : " + hal_query)
		print("Requête HAL : " + hal_query)
		i_doc = 0
		r = requests.get(url=hal_query)
		docs = r.json()["response"]["docs"]
		for doc in docs: 
			if doc["docType_s"] in types_publis_acceptes:
				# Si elle existe, on la garde avec son classement
				try:
					publi = Publication.objects.get(id_hal=doc["halId_s"])
					#print ("Modification de la publi "	publi.id_hal)
				except Publication.DoesNotExist:
					publi = Publication(id_hal=doc["halId_s"])
					#print ("Création de la publi "	publi.id_hal)
				# On modifie d'après le JSON
				publi.fromJson(doc)
				
				
				publi.save()
				# On ajoute la collection
				publi.collections.add(self)
				publi.save()
				i_doc += 1
			else:
				print (f"La publi {doc['halId_s']} est de type {doc['docType_s']} et n'est pas prise en compte")
				logger.info (f"La publi {doc['halId_s']} est de type {doc['docType_s']} et n'est pas prise en compte")

		logger.info("{0} publications ont été chargées depuis HAL dans la collection {1}".format(
			str(i_doc), self.code))
		return i_doc

	def nb_publis(self):
		return self.publication_set.count()
	
	def nb_publis_classement_periode_type(self, annee_min, annee_max, classement='all', type='all'):
		publis_periode = self.publication_set.filter(annee__gte=annee_min,
										   annee__lte=annee_max)
		if not (classement=='all'):
			publis_periode = publis_periode.filter(classement__code=classement)
		if not (type=='all'):
			publis_periode = publis_periode.filter(type=type)
		return publis_periode.count()
	
	def nb_publis_classement_annee(self,classement,annee):
		return self.publication_set.filter(classement=classement,annee=annee).count()

	def stats_reseau_coauteurs(self):
		# Prenons tous les auteurs attachés à la collection
		auteurs_collection = {}
		for auteur in self.auteurs.all():
			auteurs_collection[auteur.id] = auteur
		# Maintenant on parcourt les publis et on produit les arêtes coauteurs
		aretes = {}
		for publi in self.publication_set.all():
			for a1 in publi.auteurs.all():
				for a2 in publi.auteurs.all():
					if not (a1.id == a2.id):
						# L'arête est identifiée par la paire d'id, dans l'ordre
						id_arete = str(min(a1.id,a2.id)) + "-" + str(max(a1.id,a2.id))
						if id_arete in aretes:
							# On incrémente le nombre de liens
							aretes[id_arete]["nb_collab"] += 1
						else:
							aretes[id_arete] = {"auteur1" : a1,
												"auteur2": a2,
												"nb_collab": 1}
				
		# Pour finir on construit les arêtes du graphe au format Highgraph
		graphe =[]
		for arete in aretes.values():
			# On ne s'intéresse qu'aux arête avec un auteur de la collection
			if (arete["auteur1"].id in auteurs_collection and
				arete["auteur2"].id in auteurs_collection):
				graphe.append ({"from": arete["auteur1"].nom_complet,
						"to": arete["auteur2"].nom_complet,
						"width": arete["nb_collab"] / 2,
						"color": "orange"})
						
		# Nouvelle boucle pour trouver les auteurs solitaires
		noeuds = []
		for auteur in self.auteurs.all():
			auteur_isole = True
			for arete in graphe:
				if arete["from"] == auteur.nom_complet:
					auteur_isole = False
					break
				if arete["to"] == auteur.nom_complet:
					auteur_isole = False
					break

			if auteur_isole:
				noeuds.append ({"id": auteur.nom_complet, "color": 'orange'})

		return {"graphe": graphe, "noeuds": noeuds}

	def export(self, export_dir, annee_min, annee_max):
		'''
			Export des graphiques, fichiers Latex et biblio
		'''
		export_collection(self.code, export_dir, annee_min, annee_max)
		

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

	def __str__(self):			  # __unicode__ on Python 2
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
		print("Chargement du fichier source {0}".format(self.description))
		
		# L'index
		es_index = IndexWrapper()
		# Supprimons les refs Elastic Search
		# Sans doute inutile
		#for ref in Referentiel.objects.filter(source=self):
		#	es_index.delete_ref(ref)

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
				# La ref locale permet de s'assurer qu'il n'y a pas de collision
				ref_locale = self.identifiant_source + ":" + row['ID']
				try:
					ref = Referentiel.objects.get(ref_locale=ref_locale)
					# Qq chose exxiste ? Ca ne devrait pas arriver
					raise Exception(f"La référence {ref_locale} ne devrait pas déjà exister")
					# Remplacement de la référence 
					#ref.delete()
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

	def __str__(self):			  # __unicode__ on Python 2
		return self.titre + " (" + self.acronyme + ")"

	def __init__(self, *args, **kwargs):
		super(Referentiel, self).__init__(*args, **kwargs)

#################
class ClassementPubli(models.Model):

	"""
	   Les catégories de classement
	"""
	
	code = models.CharField(max_length=4, primary_key=True)
	libelle = models.CharField(max_length=255,)
	
	class Meta:
		db_table = "ClassementPubli"

	def __str__(self):			  # __unicode__ on Python 2
		return "%s" % (self.libelle)

	def __init__(self, *args, **kwargs):
		super(ClassementPubli, self).__init__(*args, **kwargs)

#################
class Publication(models.Model):

	"""
	   Les publications importées de Hal
	"""
	
	id_hal = models.CharField(max_length=100, primary_key=True)
	titre = models.TextField()
	annee = models.IntegerField()
	type = models.CharField(max_length=30)
	# Une publication peut être dans plusieurs collections
	collections = models.ManyToManyField(Collection, blank=True)
	# On enregistre les auteurs
	auteurs = models.ManyToManyField(Auteur, blank=True, through='AuteurPos')
	# Une chaîne avec le nom des auteurs pour la recherche
	chaine_auteurs = models.TextField(blank=True, null=True)
	revue_titre = models.TextField(blank=True, null=True)
	conf_titre = models.TextField(blank=True, null=True)
	ouvrage_titre = models.TextField(blank=True, null=True)
	number = models.CharField(max_length=255,blank=True, null=True)
	volume = models.CharField(max_length=255,blank=True, null=True)
	pages = models.CharField(max_length=30,blank=True, null=True)
	bibtex = models.TextField(blank=True, null=True)

	# Classement des publis	indicateur si le classement a été validé
	classement =  models.ForeignKey(ClassementPubli,default='I',on_delete=models.PROTECT)
	classement_valide = models.BooleanField(default=False)

	class Meta:
		db_table = "Publi"

	def __str__(self):			  # __unicode__ on Python 2
		return self.titre

	def __init__(self, *args, **kwargs):
		super(Publication, self).__init__(*args, **kwargs)


	def bibtex_hal(self):
		''' Récupération du bibtex produit par HAL 
		'''
		hal_query = QUERY_HAL_PUBLI.format(id_hal=self.id_hal)
		return requests.get(url=hal_query).content.decode('UTF-8')

	def auteurs_bibitem(self):
		# Formatage des auteurs pour la sortie bibitem
		str_auteurs = ""
		sep = ""
		for auteur in self.auteurs.all().order_by('auteurpos__position'):
			if auteur.nom is None:
				str_auteurs += sep + auteur.nom_complet
			else:
				str_auteurs += sep + initials(auteur.prenom) + " " + auteur.nom
			sep  = ", "
		return str_auteurs

	def volnum_bibitem(self):
		# Formatage du volum et du numéro pour la sortie bibitem
		volnum = ""
		if self.volume is not None and self.volume != "":
			volnum += self.volume
		if self.number is not None and self.number != "":
			volnum += f"({self.number})"
		if volnum != "":
			volnum += ", "
		return volnum

	def pages_bibitem(self):
		# Formatage du volum et du numéro pour la sortie bibitem
		if self.pages is not None and self.pages != "":
			return f"pp. {self.pages}, "
		else:
			return ""

	@staticmethod
	def stats_par_annee_type(collection, annee_min, annee_max):
		publis = Publication.get_publis_periode (collection, annee_min, annee_max)						
		# La sortie: un dictionnaire sur le type, chaque entree est un tableau avec le compte par année
		sortie = OrderedDict()
		for type_publi in TypesHAL.objects.all():
			sortie[type_publi.libelle] = list()
			for annee in range (annee_min, annee_max+1):
				nb_par_annee = 0
				# On trouve dans le résultat de la requete les publis pour cette annee et ce type				
				for publi in publis:
					if publi.type == type_publi.code and publi.annee==annee:
						nb_par_annee += 1
				sortie[type_publi.libelle].append(nb_par_annee)
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
	def get_publis_periode (collection_code, annee_min, annee_max, 
						type_publi=PUBLI_TOUS_TYPES,
						classement=PUBLI_TOUS_CLASSEMENTS):
			   
		# La requete : toutes les publis de la période
		if collection_code == TOUTES_COLLECTIONS:
			# On prend toutes les publis à condition qu'elles soient rattachées à une collection
			publis =  Publication.objects.filter(
						annee__gte=annee_min).filter(
						annee__lte=annee_max).filter(
							collections__id__gt = 0)
		else:
			publis =   Publication.objects.filter(
						annee__gte=annee_min).filter(
						annee__lte=annee_max).filter(
						collections__code=collection_code)
		
		if not (type_publi == PUBLI_TOUS_TYPES):
			# Filtre supplémentaire sur le type
			publis = publis.filter(type=type_publi)
		if not (classement == PUBLI_TOUS_CLASSEMENTS):
			# Filtre supplémentaire sur le type
			publis = publis.filter(classement=classement)
			
		#Publi en chinois....
		publis =  publis.exclude(id_hal="hal-02471589")
		return publis

	def fromJson(self, jsonDoc):
		"""
			Exctraction des données d'une publication du JSON renvoyé par Hal
		"""
		self.titre = jsonDoc["title_s"][0]
		self.annee = jsonDoc["publicationDateY_i"]
		self.type = jsonDoc["docType_s"]
		self.bibtex = jsonDoc["label_bibtex"]
		if self.type == PUBLI_REVUE:
			self.revue_titre = jsonDoc["journalTitle_s"]
		elif self.type == PUBLI_CONF:
			self.conf_titre = jsonDoc["conferenceTitle_s"]
		elif self.type == PUBLI_CHAPITRE:
			self.ouvrage_titre = jsonDoc["title_s"]
		elif self.type == PUBLI_OUVRAGE or self.type == PUBLI_DIRECTION_OUVRAGE:
			self.ouvrage_titre = jsonDoc["title_s"]
		elif self.type == PUBLI_THESE or self.type == PUBLI_HDR:
			self.ouvrage_titre = jsonDoc["title_s"]
			
		if "number_s" in jsonDoc:
			self.number = jsonDoc["number_s"]
		else:
			self.number = ''
		if "volume_s" in jsonDoc:
			self.volume = jsonDoc["volume_s"]
		if "pages_s" in jsonDoc:
			self.pages = jsonDoc["pages_s"]
		self.save()

		# Prenons les auteurs. On commence par nettoyer
		self.auteurs.clear()
		if "authIdHasStructure_fs" in jsonDoc.keys():
			chaine_auteurs = ""
			nom_auteur_courant = "xxx"
			pos_auteur = 1
			# On a une liste des structures référencées pour la publi
			for structure in jsonDoc["authIdHasStructure_fs"]:
				champs_structure = structure.split(FACET_SEP)
				id_auteur = champs_structure[0]
				champs_auteurs = id_auteur.split("-")
				id_interne = int(champs_auteurs[1])
				# Il faut encore décomposer...
				detail_structure = champs_structure[1].split(JOIN_SEP)
				id_structure = detail_structure[1]
				nom_auteur = detail_structure[0]
				
				# Créons l'auteur si c'est la première fois qu'on le trouve
				if not (nom_auteur_courant == nom_auteur):
					try:
						auteur = Auteur.objects.get(nom_complet=nom_auteur)
					except Auteur.DoesNotExist:
						auteur = Auteur(nom_complet=nom_auteur)
						auteur.save()
					# Pas d'id interne? On envoie une requête spéciale pour trouver les nom, prénom et idHal. 
					# Pas mieux...
					if id_interne > 0 and auteur.id_interne is None: 
						# La valeur non nulle indique un auteur connu de HAL: on essaie de compléter
						auteur.id_interne = id_interne
						auteur.synchro_hal()
						auteur.save()
						
					# Ajoutons l'auteur à la collection
					# Lions l'auteur à la collection avec sa position
					auteur_pos = AuteurPos (publication=self,
										auteur=auteur,
										position=pos_auteur)
					pos_auteur += 1
					auteur_pos.save()

					self.auteurs.add(auteur)
					nom_auteur_courant = nom_auteur
					chaine_auteurs +=  nom_auteur + ' '
				# Maintenant on enregistre la participation de l'auteur
				# à l'une des collections connues si c'est le cas
				try:
					coll = Collection.objects.get(id_hal=id_structure)
							# Trouvé ! L'auteur a participé à la collection
					try:
						part = Participation.objects.get(auteur=auteur,
															collection=coll)
						# Ajustons la période
						if part.date_debut.year > self.annee:
							part.date_debut = datetime.date(self.annee, 1,1)
						if part.date_fin.year < self.annee:
							 part.date_fin = datetime.date(self.annee, 12,31)
						part.save()
					except Participation.DoesNotExist:
						# Créons le lien
						part = Participation(auteur=auteur,
										collection=coll,
										date_debut=datetime.date(self.annee, 1,1),
										date_fin=datetime.date(self.annee, 12,31)
										)
						part.save()
				except Collection.DoesNotExist:
					# On ne connait pas cette collection, on continue
					pass
			self.chaine_auteurs = chaine_auteurs
			self.save()

class AuteurPos(models.Model):
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)
	position = models.IntegerField(default=1)


#### Utilitaires export

def export_collection(code_collection, export_dir, annee_min, annee_max):
		'''
			Export des graphiques, fichiers Latex et biblio
		'''
		periode = range (annee_min, annee_max+1)
		
		# On  crée le répertoire pour la collection s'il n'existe pas
		coll_dir = os.path.join(export_dir, code_collection)
		if not os.path.isdir(coll_dir):
			os.mkdir (coll_dir)

		# Nettoyage 
		# Copie du fichier makefile
		makefile = os.path.join(settings.BASE_DIR,"publis", "templates", "publis", "export", "Makefile")
		with open(makefile, 'r', encoding="UTF-8") as file :
			filedata = file.read()
			filedata = filedata.replace('{equipe}', code_collection)
		with open(os.path.join(coll_dir,"Makefile"), 'w', encoding="UTF-8") as file:
  			file.write(filedata)
		# On copie le fichier de recap blblio en substituant le nom de la collection
		la_biblio = os.path.join(settings.BASE_DIR,"publis", "templates", "publis", "export", "la_biblio.tex")
		with open(la_biblio, 'r', encoding="UTF-8") as file :
			filedata = file.read()
			filedata = filedata.replace('{equipe}', code_collection)
		with open(os.path.join(coll_dir,f"biblio_{code_collection}.tex"), 'w', encoding="UTF-8") as file:
  			file.write(filedata)
  
   			
		### Export des graphiques et docs. On commence par nettoyer les dossiers
		doc_publis_dir = os.path.join(coll_dir, "docs_publis")
		shutil.rmtree(doc_publis_dir)
		os.mkdir (doc_publis_dir)
		stats_publis_dir = os.path.join(coll_dir, "stats_publis")
		shutil.rmtree(stats_publis_dir)
		os.mkdir (stats_publis_dir)

		export_fichiers = UtilExport("publis/export", doc_publis_dir)
		export_graphiques = UtilExport("publis/export", stats_publis_dir)
		
		# Astuce Cédric
		if code_collection == "labo":
 			code_collection = TOUTES_COLLECTIONS

		# Lecture des modèles de graphiques 
		export_graphiques.exportDiagBarres(list(periode), Publication.stats_par_annee_type(
				code_collection, annee_min, annee_max),  "par_annee_type.json")
		export_graphiques.exportDiagBarres(list(periode), Publication.stats_par_annee_classement(
				code_collection, annee_min, annee_max),  "par_annee_classement.json")
		export_graphiques.exportCamembert(Publication.stats_par_classement(
			code_collection, annee_min, annee_max), "par_classement.json")
	
		### Export des fichiers biblio
		synthese_publis = {}
		for classement in ClassementPubli.objects.all():
			# Toutes les publis pour le classement
			publis = Publication.get_publis_periode(code_collection, annee_min, annee_max, classement=classement)
			donnees = {"classement": classement.libelle, "constants": publi_constants,"publis": publis, "titre_section": ""}
			export_fichiers.exportFichier('bibliography.tex', donnees, f"biblio_{classement.code}.tex")
			
			nb_pub_classement = Publication.get_publis_periode(code_collection, 
											annee_min, annee_max, 
											classement=classement).count()
			
			synthese_publis[f"nb_{classement.code}"] = nb_pub_classement
			# Pour les articles et conf, on crée un fichier détaillé par type-classement
			for type in [PUBLI_CONF, PUBLI_REVUE, PUBLI_CHAPITRE,PUBLI_OUVRAGE,PUBLI_BREVET,PUBLI_DIRECTION_OUVRAGE,PUBLI_ACTES,PUBLI_LOGICIEL]:
				publis_classement_type = Publication.get_publis_periode(code_collection, annee_min, annee_max, 
											type_publi=type,classement=classement)
				publis_type = Publication.get_publis_periode(code_collection, annee_min, annee_max, 
											type_publi=type)

				nb_pub_classement_type = publis_classement_type.count()
				nb_pub_type = publis_type.count()
				synthese_publis[f"nb_{classement.code}_{type}"] = nb_pub_classement_type
				synthese_publis[f"nb_{type}"] = nb_pub_type

				if type == PUBLI_REVUE:
					titre_section = f"Revues"
				elif type == PUBLI_CONF:
					titre_section = f"Conférences"
				elif type == PUBLI_CHAPITRE:
					titre_section = f"Chapitres"
				elif type == PUBLI_OUVRAGE:
					titre_section = f"Ouvrages"
				elif type == PUBLI_DIRECTION_OUVRAGE:
					titre_section = f"Directions d'ouvrage"
				elif type == PUBLI_ACTES:
					titre_section = f"Actes de conférence"
				elif type == PUBLI_BREVET:
					titre_section = f"Brevets"
				elif type == PUBLI_LOGICIEL:
					titre_section = f"Logiciels"
				titre_section += f" ({nb_pub_classement_type} publications)"
				if nb_pub_classement_type > 0:
					donnees = {"classement": classement.libelle, "constants": publi_constants,
							  "publis": publis_classement_type,"titre_section": titre_section}
					export_fichiers.exportFichier('bibliography.tex', donnees, f"biblio_{classement.code}_{type}.tex")
		
		### Export de la synthèse biblio
		export_fichiers.exportFichier('synthese_publis.tex', synthese_publis,
										"synthese_publis.tex", False)
		 
		### Export des theses et HDR
		publis_theses = list(Publication.get_publis_periode(code_collection, annee_min, annee_max, type_publi=PUBLI_THESE))
		publis_hdr =  list(Publication.get_publis_periode(code_collection, annee_min, annee_max, type_publi=PUBLI_HDR))
		publis_theses.extend(publis_hdr)
		donnees = {"classement": "Thèses et HDR",
					 "publis": publis_theses
				}
		export_fichiers.exportFichier('bibliography.tex', donnees,
										f"theses.tex")
		### Export du referentiel	
		if code_collection == TOUTES_COLLECTIONS:
			export_fichiers.exportFichier('referentiel.tex', 
									{"sources": Source.objects.filter(type_source=SOURCE_INTERNE)}
									)
			
		# Fichiers bibtex produits par HAL: beaucoup trop long
		#filehandle.writelines([publi.bibtex_hal(), "\n"])


# Obtenir des initiales à la place d'une suite de prénoms
def initials(nom_complet):
	if (len(nom_complet) == 0):
	  return ""
	initiales = ""
	comps = nom_complet.strip().replace("  "," ").split(" ")
	for name in comps:
		initiales = initiales + name[0].upper()+"."
	return initiales

class UtilExport:
	'''
		Pour produire un fichier à partir d'un template et de données
	'''
	
	def __init__(self, dir_input, dir_output) :
		self.dir_in = dir_input
		# Creation si n'existe pas
		if not os.path.isdir(dir_output):
			os.mkdir (dir_output)
		self.dir_out = dir_output

		# Chargement des types de graphiques
		self.diag_barres = SimpleTemplateResponse (os.path.join(self.dir_in,'diagramme_barres.json'),{})
		self.diag_camembert = SimpleTemplateResponse (os.path.join(self.dir_in,'diagramme_camembert.json'),{})
		self.diag_barres_stacked = SimpleTemplateResponse (os.path.join(self.dir_in,'diagramme_barres_stacked.json'),{})
		self.diag_reseau = SimpleTemplateResponse (os.path.join(self.dir_in,'diagramme_reseau.json'),{})
		
	def exportFichier(self, template, context, fichier_sortie="", protection_latex=True):		
		if fichier_sortie == "":
			fichier_sortie = template
			
		# Caractères à protéger en Latex
		replacements_dict = {
    		'&': '\&',
      		'_': '\_',
#      		'ž': 'z',
#      		'ć': 'c',
      		'∞': '$\infty$',
 		}
		transcripteur = str.maketrans(replacements_dict)
		
		t = SimpleTemplateResponse(os.path.join(self.dir_in, template), context)
		contenu_brut = t.rendered_content
		if protection_latex:
			contenu_brut= contenu_brut.translate(transcripteur)
			contenu_brut = contenu_brut.replace('\\xa0', ' ').replace('ž','z'
															).replace('ć', 'c'
															).replace ("{ ", "{"
															).replace (" }", "}"
															).replace ("#", "\#"
															).encode('utf-8')
		else:
			contenu_brut = contenu_brut.encode('utf-8')
		with io.open(os.path.join(self.dir_out, fichier_sortie), 'w',encoding='utf8') as filehandle:
			filehandle.write(contenu_brut.decode("utf-8") )
			
	def exportDiagBarres(self, periode, donnees, fichier_sortie):		
		self.diag_barres.context_data["chart_annees"] = periode
		self.diag_barres.context_data["chart_donnees"] = donnees
		with open(os.path.join(self.dir_out, fichier_sortie), 'w',encoding='utf8') as filehandle:
			filehandle.write(str(self.diag_barres.rendered_content))

	def exportCamembert(self, donnees, fichier_sortie):		
		self.diag_camembert.context_data["chart_donnees"] = donnees
		with open(os.path.join(self.dir_out, fichier_sortie), 'w',encoding='utf8') as filehandle:
			filehandle.write(str(self.diag_camembert.rendered_content))
	def exportDiagBarresStacked(self, periode, donnees, fichier_sortie):			
		self.diag_barres.context_data["chart_annees"] = periode
		self.diag_barres_stacked.context_data["chart_donnees"] = donnees
		with open(os.path.join(self.dir_out, fichier_sortie), 'w',encoding='utf8') as filehandle:
			filehandle.write(str(self.diag_barres_stacked.rendered_content))

