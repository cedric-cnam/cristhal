import os
import logging
import zipfile
from io import BytesIO

# Django import
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from collections import namedtuple
from django.forms import modelformset_factory
from django.conf import settings

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse

from django.db import connection, connections

from .constants import *
from .models  import Collection, Referentiel, Publication, Source, Config, Auteur
from .IndexWrapper import IndexWrapper

from  .forms import ClassementPubliForm, PubliSearchForm
from publis.constants import CHOIX_SOURCES
from publis.models import ClassementPubli
from _ast import alias


# Un journaliseur 
logger = logging.getLogger(settings.LOGGER_NAME)

def menu_local(contexte):
	""" 
		Création du menu local selon le contexte (la fonction appelée)
	"""
	menu_local = []
	menu_local.append ({"url": reverse('publis:collections'), "lien": "<b>Collections</b>", "niveau": 1})
	menu_local.append ({"url": reverse('publis:referentiel'), "lien": "<b>Référentiel</b>", "niveau": 1})
	menu_local.append ({"url": reverse('publis:instructions'), "lien": "<b>Classement collections</b>", "niveau": 1})
	menu_local.append ({"url": reverse('publis:publications'), "lien": "<b>Publications</b>", "niveau": 1})
	menu_local.append ({"url": "#", "lien": "<hr/>"})
	if contexte=="collections" :
		menu_local.append({"url": reverse('publis:stats_generales'), 
							   "lien": "Statistiques générales", "niveau": 2})
		menu_local.append({"url": reverse('admin:publis_collection_add'), 
							   "lien": "Ajout d'une collection", "niveau": 2})
		for coll in Collection.objects.all():
			coll_url = reverse('publis:stats_collection', kwargs={'code_collection': coll.code})
			menu_local.append({"url": coll_url, "lien": coll.nom, "niveau": 2})
	if contexte=="référentiel":
		menu_local.append({"url": reverse('admin:publis_source_add'), 
							   "lien": "Ajout d'une source", "niveau": 2})
		menu_local.append ({"url": reverse('publis:recherche'), "lien": "Recherche dans le référentiel", "niveau": 2})
	if contexte=="classement":
		for coll in Collection.objects.all():
			coll_url = reverse('publis:classement', kwargs={'code_collection': coll.code})
			menu_local.append({"url": coll_url, "lien": coll.nom, "niveau": 2})
	if contexte=="publications" :
		menu_local.append({"url": reverse('publis:publications'), 
							   "lien": "Recherche par formulaire", "niveau": 2})
		menu_local.append({"url": reverse('publis:sql'), 
							   "lien": "Recherche par SQL", "niveau": 2})
	return menu_local


@login_required
def collections(request):
	context = {
				"collections": Collection.objects.all(),
				 "titre": "Liste des collections",
				 "sous_menu": "collections",
				 "menu_local": menu_local("collections")
			   }
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
	#  Vérifications de la configuration
	
	if not os.path.isdir(settings.MEDIA_ROOT):
		context["message"] = alerte("Attention: le répertoire {0} de stockage des fichiers exportés / importés n'existe pas".format(
			settings.MEDIA_ROOT))
	elif not os.access(settings.MEDIA_ROOT, os.W_OK):
			context["message"] = "Le répertoire {0} doit permettre l'écriture de fichiers ".format(
			settings.MEDIA_ROOT)
	elif not os.path.isdir(config.repertoire_export):
			# On essaie de le créer, normalement c'est dans MEDIA
			os.mkdir (settings.EXPORT_DIR)

	# Si paramètre, on déclenche une nouvelle synchro
	if request.GET.get ("synchro", "0") == "1":
		collection = Collection.objects.get (code=request.GET.get ("code"))
		nb_publis = collection.synchro_hal()
		
		# Elimination des doublons dans les auteurs
		connection = connections['default']
		requete_sql ="""select id_hal, nom_complet, count(*) as nb_alias 
		                 from Auteur where id_hal is not null group by id_hal having count(*) > 1
		               """
		with connection.cursor() as cursor:
			cursor.execute(requete_sql)
			for auteur in namedtuplefetchall(cursor):
				# On a trouvé un auteur avec plusieurs alias
				print ("On a trouve un doublon d'alias pour " + auteur.nom_complet)
				i_alias = 0
				for alias in Auteur.objects.filter(id_hal=auteur[0]):
					#print ("On a trouve l'alias " + str(alias.id_hal))
					if i_alias == 0:
						# C'est celui là qu'on garde
						le_bon = alias
					else:
						#print ("Recherche des publis pour l'alias " + str(alias.id))
						for publi in Publication.objects.filter(auteurs__id=alias.id):							
							#print (f"Remplacement de {alias.id} par {le_bon.id} dans {publi.id_hal}")
							with connection.cursor() as replace:
								replace.execute(f"delete from  publis_auteurpos " +
											    f" where auteur_id={le_bon.id} and publication_id='{publi.id_hal}'")
								replace.execute(f"update publis_auteurpos set auteur_id={le_bon.id} " +
											    f" where auteur_id={alias.id} and publication_id='{publi.id_hal}'")
						with connection.cursor() as replace2:
							replace2.execute(f"delete from Participation where auteur_id={alias.id}")
						alias.delete()
						
					i_alias+=1

		context["message"] = '''{0}  publications ont été synchronisées 
						depuis HAL dans la collection {1} 
						pour la période {2}-{3}.'''.format(
				 str(nb_publis), collection.code, config.annee_min_publis,
				 config.annee_max_publis)
	# Si export, on exporte !
	if request.GET.get ("export", "0") == "1":
		collection = Collection.objects.get (code=request.GET.get ("code"))
		contenu_zip = export(collection, context)
		resp = HttpResponse(contenu_zip.getvalue(), content_type = "application/x-zip-compressed")
		resp["Content-Disposition"] = "attachment; filename=%s" %  (collection.code + ".zip")
		return resp 

	# Affichage des collections
	return render(request, 'publis/collections.html', context)


@login_required
def stats_generales(request):
	context = {
				"collections": Collection.objects.all(),
				 "titre": "Statistiques générales",
				 "sous_menu": "collections",
				 "menu_local": menu_local("collections")
			   }
	
	# Un peu de stats
	# La période est donnée par la config
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
	context["annees"] = list(range (config.annee_min_publis, config.annee_max_publis+1))
	context["stats_revues_par_collection"] = Config.stats_collections(config.annee_min_publis, 
																	  config.annee_max_publis,
																	  PUBLI_REVUE)
	context["stats_confs_par_collection"] = Config.stats_collections(config.annee_min_publis, 
																	  config.annee_max_publis,
																	  PUBLI_CONF)

	context["stats_type_publis"] = Config.stats_types_publis()
	context["stats_annee_type"] = Publication.stats_par_annee_type(TOUTES_COLLECTIONS, 
																   config.annee_min_publis, 
																   config.annee_max_publis)
	context["stats_annee_classement"] = Publication.stats_par_annee_classement(TOUTES_COLLECTIONS, 
																   config.annee_min_publis, 
																   config.annee_max_publis)

	# Affichage des collections
	return render(request, 'publis/stats_generales.html', context)


@login_required
def stats_collection(request, code_collection):
	context = {"titre": "Statistiques sur la collection " + code_collection.upper(), 
			   "collections": Collection.objects.all(),
								"sous_menu": "collections",
				  "menu_local": menu_local("collections")
				}
	# La période est donnée par la config
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)

	context["collection"] = Collection.objects.get(code=code_collection)
	context["annees"] = list(range (config.annee_min_publis, config.annee_max_publis+1))
	context["stats_annee_type"] = Publication.stats_par_annee_type(code_collection, 
																   config.annee_min_publis, 
																	config.annee_max_publis)
	context["stats_annee_classement"] = Publication.stats_par_annee_classement(code_collection, 
																				config.annee_min_publis,  
																				 config.annee_max_publis)
	context["stats_classement"] = Publication.stats_par_classement(code_collection, 
																	config.annee_min_publis,  
																	config.annee_max_publis)
	context["stats_reseau_coauteurs"] = context["collection"].stats_reseau_coauteurs()
	
	return render(request, 'publis/stats_collection.html', context)

@login_required
def referentiel(request):
	context = {"titre": "Référentiel ", 
			   "collections": Collection.objects.all(),
			   "sources": Source.objects.all(),
			   "types_sources": CHOIX_SOURCES,
				 "sous_menu": "référentiel",
				  "menu_local": menu_local("référentiel")
				}

	if request.method == 'GET' and 'id_source' in request.GET:
		source = Source.objects.get(id=request.GET['id_source'])
		try:
			nb_refs = source.chargement_fichier()
			context["message"]="%s références ont été chargées depuis le fichier source %s " %  (
				str(nb_refs), os.path.basename(source.fichier.name))
		except Exception as ex:
			context["message"] = "Erreur pendant le chargement du fichier : {0}. Avez-vous bien vérifié le format ?".format(
				str(ex))
					
		
	return render(request, 'publis/referentiel.html', context)

@login_required
def recherche(request):
	context = {"titre": "Recherche dans le référentiel des publications", 
			   "collections": Collection.objects.all(),
			   "sources": Source.objects.all(),
			   "types_sources": CHOIX_SOURCES,
			   "sous_menu" : "recherche",
				  "menu_local":  menu_local("référentiel")
				}
	# Définition du menu local
	context["menu_local"].append ({"url": reverse('publis:collections'), "lien": "<b>Collections</b>"})
	context["menu_local"].append ({"url": "#", "lien": "<hr/>"})
	context["menu_local"].append ({"url": reverse('publis:referentiel'), "lien": "<b>Référentiel</b>"})
	context["menu_local"].append ({"url": reverse('publis:recherche'), "lien": "Recherche dans le référentiel"})

	context["requete"]= "IEEE ACM Transactions on Networking"
	context["checked_revue"] = "checked"
	if request.GET.get('envoi_requete'):
		context["requete"] = request.GET.get("requete")
		if request.GET.get('choix_type') == PUBLI_CONF:
			context["checked_conf"] = "checked"

		# Recherche avec ElasticSearch
		wrapper = IndexWrapper()
		context["refs"] = wrapper.search(request.GET.get("requete"), request.GET.get('choix_type'))
		context["resultat"] = True
	return render(request, 'publis/recherche.html', context)


@login_required
def instructions(request):
	context = {"titre": "Instructions pour le classement des publications", 
			   "collections": Collection.objects.all(),
			   "sources": Source.objects.all(),
			   "types_sources": CHOIX_SOURCES,
				  "menu_local": menu_local("classement"),
					"sous_menu" : "classement",
				}
	return render(request, 'publis/instructions.html', context)

@login_required
def classement(request, code_collection):
	context = {"titre": "Classement des publications de la collection " + code_collection.upper(), 
			   "collections": Collection.objects.all(),
							 "sous_menu" : "classement",
				  "menu_local": menu_local("classement")
				}
	# Cherchons la configuration pour avoir des valeurs par défaut
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
	context["annees"] = list(range (config.annee_min_publis, config.annee_max_publis+1))

	# Sur validation, envoyer un messqge au responsable 
	
	# Formulaire pour effectuer le classement
	PublisFormset = modelformset_factory(
		Publication, form=ClassementPubliForm, extra=0)

	if request.method == 'POST':
		# On effectue la mise à jour
		formset = PublisFormset(request.POST,)
		if formset.is_valid():
			formset.save()
		else:
			print(formset.errors)
	wrapper = IndexWrapper()
	
	# Creation du jeu de données et du formulaire pour le classement
	# On ne classe que les revues et conf puisqu'il n'y a pas de référentiel pour les autres
	publis = Publication.objects.filter(
						annee__gte=config.annee_min_publis).filter(
						collections__code=code_collection).filter(type=PUBLI_CONF
						) |  Publication.objects.filter(
						annee__gte=config.annee_min_publis).filter(
						collections__code=code_collection).filter(type=PUBLI_REVUE
						)

	context["classement_formset"] = PublisFormset (queryset=publis)

	context["matches"] = []
	context["bestrefs"] = []
	context["publis"] = publis
	for publi in publis:
		if not (publi.type == PUBLI_CONF or publi.type == PUBLI_REVUE):
			continue
		
		if publi.type == PUBLI_CONF:
			refs = wrapper.search(publi.conf_titre, PUBLI_CONF)
		elif publi.type == PUBLI_REVUE:
			if publi.revue_titre is None:
				publi.revue_titre = "XXX "
			refs = wrapper.search(publi.revue_titre, PUBLI_REVUE)
		
		# On cherche la meilleure ref pour chaque  types de source
		trouve_core = False
		trouve_scimago = False
		trouve_interne = False
		meilleures_ref = []
		scores_scimago = []
		sources_scimago = []
		refs_scimago = []
		for ref in refs:
			if ref.type_source == SOURCE_CORE and not (trouve_core):
				meilleures_ref.append(ref)
				trouve_core = True
			elif ref.type_source == SOURCE_SCIMAGO:
				# On peut trouver une bonne ref dans chaque source SCIMAGO
				if ref.source not in sources_scimago:
					refs_scimago.append(ref)
					sources_scimago.append(ref.source)
					scores_scimago.append(ref.meta.score)
			elif ref.type_source == SOURCE_INTERNE and not (trouve_interne):
				meilleures_ref.append(ref)
				trouve_interne = True
		# Traitement des sources SCIMAGO. On garde les trois meilleures
		scores_scimago.sort(reverse=True)
		if len(scores_scimago) > 0:
			min_score= min(scores_scimago[:3])
			for ref_scim in refs_scimago:
				if ref_scim.meta.score >= min_score:
					meilleures_ref.append(ref_scim)
		bestref = {"id_hal": publi.id_hal, "meilleures_ref": meilleures_ref}
		context["bestrefs"].append(bestref)

	return render(request, 'publis/classement.html', context)


@login_required
def publications(request):
	context = {"titre": "Interface de recherche des publications", 
			   "collections": Collection.objects.all(),
			   "types_sources": CHOIX_SOURCES,
			   "classement_publis": ClassementPubli.objects.all(),
					"sous_menu" : "publications",
				  "menu_local": menu_local("publications")
				}
	
	# Cherchons la configuration pour avoir des valeurs par défaut
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
	
	# Attention au cas où aucune collection n'existe
	if len(context["collections"]) == 0:
		coll_def = None
	else:
		coll_def = context["collections"][0]
	initial_dict = {
		"annee_min" : config.annee_min_publis,
		"annee_max" : config.annee_max_publis,
		"collection" : coll_def,
		"classement" : context["classement_publis"][0],
		}

	# Initialisation du formulaire de recherche
	context["form_recherche"] = PubliSearchForm (None, initial=initial_dict)

	if request.method == "POST":
		# Récupération des données soumies
		form = PubliSearchForm(request.POST)
		if form.is_valid():
			# Effectuons la recherche
			context["resultat"] = Publication.objects.filter(
							annee__gte=form.cleaned_data["annee_min"]).filter(
							annee__lte=form.cleaned_data["annee_max"])
			if not (form.cleaned_data["classement"] == 'tous'):
				context["resultat"] = context["resultat"].filter(
							classement__code=form.cleaned_data["classement"])
			if not (form.cleaned_data["collection"] == 'toutes'):
				context["resultat"] = context["resultat"].filter(
							collections__code=form.cleaned_data["collection"])
			if not (form.cleaned_data["auteur"] =='') :
				res = []
				for pub in context["resultat"]:
					if pub.chaine_auteurs is not None and form.cleaned_data["auteur"].upper() in pub.chaine_auteurs.upper():
						res.append(pub)
				context["resultat"] = res
		# Le formulaire est réinitialisé avec les données soumises
		context["form_recherche"] = PubliSearchForm(None, initial=form.cleaned_data)
		
	return render(request, 'publis/publications.html', context)


@login_required
def sql(request):
	context = {"titre": "Recherche directe par SQL", 
			   "collections": Collection.objects.all(),
					"sous_menu" : "publications",
				  "menu_local": menu_local("publications"),
				"requete_sql": "select * from Publi"}
	context["cols"] = []
	context["rows"] = []
	
	if request.GET.get('envoi_requete'):
		connection = connections['lecteur']
			
		# On prend la requête
		context["requete_sql"] = request.GET.get('requete_sql') 
		# On ajoute une clause "limit"
		requete_sql = context["requete_sql"].replace(";", " ") + " limit 200 "
		
		with connection.cursor() as cursor:
			try:
				cursor.execute(requete_sql)
				context["rows"] = namedtuplefetchall(cursor)
				for coldesc in cursor.description:
					context["cols"].append(coldesc[0])
				context["resultat"] = True
				context["erreur"] = False
			except Exception as exc : 
				context["erreur"] = True
				context["message"] = "Erreur: " + str(exc)
		
	return render(request, 'publis/sql.html', context)


def export(coll, context):
	'''
		Export des données d'une collection
	'''

	# Cherchons la configuration pour avoir des valeurs par défaut
	config = Config.objects.get(code=CODE_CONFIG_DEFAUT)
	coll_dir = os.path.join(config.repertoire_export, coll.code)

	# TODO: mieux vaut effacer le répertoire
	coll.export(config.repertoire_export, config.annee_min_publis, config.annee_max_publis)

	# Pour finir on met tout ça dans un zip et on envoie
	contenu_zip = BytesIO()
	zf = zipfile.ZipFile(contenu_zip, "w")
	for file in os.listdir(coll_dir):   
		if file.endswith(".json") or file.endswith(".bib") or file.endswith(".tex"):
			zf.write(os.path.join(coll_dir,file), file)		 
	zf.close()

	return contenu_zip

#
# Pour mettre un message en rouge (mieux: définir un CSS)
#
def alerte (message):
	return "<font color='red'>{0}</font>".format(message)


# Pour obtenir des nuplets nommés
#
def namedtuplefetchall(cursor):
	"Return all rows from a cursor as a namedtuple"
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]
