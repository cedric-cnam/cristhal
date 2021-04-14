.. _chap-install:

############
Installation
############

CristHAL est une application Python s'appuyant sur le *framework* Django (https://www.djangoproject.com/).  
Les composants de l'architecture technique sont illustrés par la :numref:`archiTechnique`.

.. _archiTechnique:
.. figure:: ./figures/ArchiTechnique.png       
        :width: 90%
        :align: center
   
        Les composants techniques

Tous ces composants sont des logiciels libres qui fonctionnent sur toutes les plateformes.

  - Le cœur du système est une application Python/Django. 
  - Le stockage des données est assuré par MySQL (http://mysql.com).
  - Un moteur de recherche, ElasticSearch (https://www.elastic.co/fr/elasticsearch/), 
    est utilisé pour la procédure d'appariement.
  - Enfin un serveur Web quelconque, doté d'une passerelle WSGI, est requis pour une mise en production.


Pour une installation initiale, il n'est pas nécessaire de disposer d'un serveur Web: un serveur intégré
à Django permet d'effectuer la configuration et les tests, ce que nous appelons "mise en route" 
dans ce qui suit. Pour une mise en production, un vrai serveur web s'impose, ainsi que quelques précautions
de configuration.

À l'exception (très relative) d'ElasticSearch, cette architecture est très classique et utilisé par des millions
de sites web. On trouve donc de très nombreuses ressources pour la configuration des différents compsosants. Ce
qui suit se concentre donc sur la partie spécifique à CristHAL.


*************
Mise en route
*************

On suppose donc que vous disposez d'une machine équipée de Python (version au moins 3.6), et d'un accès 
à un serveur MySQL et à un serveur ElasticSearch. Pour MySQL il est nécessaire de créer 
une base et deux  comptes

 - un compte administrateur disposant de tous les droits sur la base
 - un compte ne disposant que des droits de lecture ; ce deuxième compte
   est utilisé pour exécuter des requêtes SQL saisies dans un formulaire: mieux vaut
   éviter les fausses manœuvres.

Voici des exemples de commandes (elles se trouvent dans 
``install/creationDb.sql``).

.. code-block:: sql

    /* Nom de base à reporter dans cristhal/local_settings.py */
    create database cristhal CHARACTER SET utf8;

    /*
    * Nom admin et mot de passe à changer et reporter dans cristhal/local_settings.py
    */
    grant all privileges on cristhal.* to cristhalAdmin identified by 'mdpCristhal';

   /* Compte avec droits de lecture uniquement, pour les requêtes SQL */
    grant select on cristhal.* to cristhalLecteur identified by 'mdpLecteur';

.. important:: Ne les copiez pas telles quelles ! *Changez au moins le mot de passe*

Pas besoin de créer l'index pour ElasticSearch, CristHAL s'en charge à la première connexion.

Le code de CristHAL peut être récupéré sur
https://github.com/cedric-cnam/cristhal. Installez-le dans un répertoire que nous appelerons ``cristhaldir``.


.. note:: Dans tout ce qui suit, ``python`` et ``pip`` s'appliquent à Python3,
   et correspondent dans certains environnements aux commandes ``python3`` et ``pip3``.
 
La première chose à faire est d'installer les modules Python nécessaires à CristHAL. Ils sont 
énumérés dans le fichier ``requirements.txt``.

.. code-block:: bash

    pip3 install -r requirements.txt

On peut passer à la configuration des accès serveurs.

Accès MySQL et ElasticSearch
============================

Les accès aux serveurs sont configurés dans des fichiers du répertoire ``cristhaldir/cristhal``. La configuration
générale est dans le fichier ``settings.py``, la configuration spécifique à un site doit
être placée dans un fichier ``local_settngs.py`` dont les options prennent priorité sur le premier.

Dans ``cristhaldir/cristhal``, copiez ``local_settings_exemple.py`` en ``local_settings.py``. Puis éditez
ce dernier.

La configuration d'accès au serveur MySQL est indiquée dans la variable ``DATABASES``. Reportez-y 
vos paramètres de site.

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nom_bd_locale',
            'USER': 'admin_bd_locale',
            'PASSWORD': 'mdp_bd_locale',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'STRICT_ALL_TABLES',
            },
        },
    'lecteur': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'NAME': 'cristhal',
        'USER': 'cristhalLecteur',
        'PASSWORD': 'mdpLecteur',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
  }

.. note:: Il faut définir deux connexions, une pour l'administrateur, et l'autre
   pour le compte 'lecteur'. Ne changez pas les noms des connexions.

La configuration d'accès au serveur ElasticSearch est indiquée dans les variables suivantes.
Vous pouvez conserver la valeur de  ``ES_INDEX_REF`` si vous le souhaitez.  Indiquez 
les autres paramètres dans ``ELASTIC_SEARCH``.

.. code-block:: python

      ES_INDEX_REF = "cristhal"
      ELASTIC_SEARCH = {"host": "localhost", "port": 9200, 
                  "index": ES_INDEX_REF}

Certains fichiers (les CSV des sources du référentiel notamment) sont 
stockés dans un répertoire local spécifié par le paramètre ``MEDIA_ROOT``.
Par défaut il est dans ``cristhaldir``.

.. code-block:: python
 
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Il est préférerable d'indiquer un répertoire distinct de l'application. Dans
tous les cas, le compte utilisateur sous lequel l'application s'exécute doit
avoir le droit d'y écrire.

Un dernier paramètre à régler est l'emplacement des fichiers journaux. Le chemin
proposé par défaut est:

.. code-block:: python

     LOG_DIR = '/var/log'
    
Indiquez le chemin qui convient (et vérifiez qu'il est possible d'écrire dans ce répertoire pour
le processus qui exécute CristHAL). 


Création du schéma et initialisation
====================================

Si votre configuration est correcte, vous devez pouvoir exécuter la commande suivante
dans ``cristhaldir``.

.. code-block:: bash 

    python manage.py migrate
    
C'est une commande Django qui crée (ou modifie) le schéma. Si la connexion au serveur MySQL échoue, 
vous le saurez tout de suite. Sinon, votre schéma est créé. 

C'est presque prêt! Maintenant ajoutez un super-utilisateur avec une autre commande Django.

.. code-block:: bash

     python manage.py createsuperuser

Suiviez les instructions (et mémorisez le compte !). Pour finir, 
CristHAL propose une autre commande pour créer une configuration initiale.

.. code-block:: bash

     python manage.py init_publis

Quelques messages vous indiquent les opérations effectuées. 

Il ne reste qu'à lancer le serveur intégré à Django.

.. code-block:: bash

     python manage.py runserver

Pas d'erreur ? Alors vous pouvez accèder avec un navigateur quelconque à http://localhost:8000
et vous devriez obtenir l'écran de la :numref:`ecran-accueil` (qui peut évoluer avec les versions).

.. _ecran-accueil:
.. figure:: ./figures/ecran-accueil.png       
        :width: 90%
        :align: center
   
        L'écran d'accueil
        
Vous pouvez vous connecter avec le compte super-utilisateur défini précédemment.
Tout est prêt pour commencer à utiliser l'application (en mode 'tests': pour la mise en production
voir ci-dessous). Commençons par l'interface d'administration.

L'interface d'administration
============================

Une fois connecté avec un compte d'administration, un menu ``Admin`` apparaît
(:numref:`ecran-accueil`). 


.. _ecran-accueil2:
.. figure:: ./figures/ecran-accueil2.png       
        :width: 90%
        :align: center
   
        L'écran d'accueil après connexion

Ce menu donne accès aux fonctions de création et de mise à jour
des principaux objets configurant CristHAL: utilisateurs, codification, collections,
sources (du référentiel, etc.)

La création des groupes (définissant des droits d'accès) et des utilisateurs est 
une fonction standard de Django. Vous pouvez créer quelques utilisateurs: seuls ceux
dotés du droit 'super-utilisateur' pourront accéder au menu d'administration.

Les autres formulaires sont gérés automatiquement par Django, mais donnent
accès aux données spécifiques. Pour vous rôder vous pouvez
accéder à l'interface de définition des configurations. 

Il doit exister au moins une configuration, nommée ``défaut``. Elle est créée à l'initialisation
de CristHAL et contient plusieurs paramètres:

  - L'adresse des services web HAL (ne pas modifier en principe)
  - La période (année min et max) de récolte des publications.

Au-delà de la configuration, tout le paramétrage de CristHAL se fait via cette interface
d'administration.

.. important:: Pour revenir au site principal à partir de l'interface d'administration, il faut
   suivre le lien 'View site' en haut à droite.

******************
Mise en production
******************

Pour une mise en production, il faut associer CristHAL à un serveur Web, et changer un peu la
configuration.


Le serveur web
==============

CristHAL est une application Django standard, et l'association avec un serveur ne
présente aucune spécificité. Dans le répertoire ``cristhaldir/cristhal`` se trouve
un fichier ``wsgi.py`` qui sert à créer une passerelle WSGI avec un serveur
comme Apache, Nginx ou Gunicorn.

La documentation  explique en détail la procédure pour ces différents serveurs:
https://docs.djangoproject.com/fr/3.1/howto/deployment/wsgi/.

Configuration en production
===========================

Il faut évidemment adapter la configuration pour s'assurer de la protection de l'application
si elle est exposée sur le Web. Là encore, la documentation
https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/ nous dit l'essentiel,
et on trouve de très nombreux tutoriels qui détaillent les précautions à prendre.

La configuration de CristHAL peut se placer dans le fichier ``local_settings.py`` (vous pouvez
en créer un spécifique à l'environnement de production). Voici quelques 
modifications essentielles. La première chose à faire
est de quitter le mode *debug*.

.. code-block:: python

    Debug = False
    
Ajouter également une clé secrète. Une bonne pratique est de la définir comme 
variable d'environnement et de la paramétrer ainsi.

.. code-block:: bash 

     SECRET_KEY = os.environ['SECRET_KEY']

Enfin il faut spécifier les domaines servis par l'application dans le tableau suivant.

.. code-block:: bash 

    ALLOWED_HOSTS = []
    



