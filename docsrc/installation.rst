
   
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
  - Le stockage des données est assuré par MySQL (http://mysql.com)
  - Un moteur de recherche, ElasticSearch (https://www.elastic.co/fr/elasticsearch/), 
    est utilisé pour la procédure d'appariement.
  - Enfin un serveur Web quelconque, doté d'une passerelle WSGI, est requis pour une mise en production 


Pour une installation initiale, il n'est pas nécessaire de disposer d'un serveur Web: un serveur intégré
à Django permet d'effectuer la configuration et les tests, ce que nous appelons "mise en route" 
dans ce qui suit. Pour une mise en production, un vrai serveur web s'impose, ainsi que quelques précautions
de configuration.


À l'exception (très relative) d'ElasticSearch, cette architecture est très classique et utilisé par des millions
de sites web. On trouve donc de très nombreuses ressources pour la configuration des différents compsosants. Ce
qui suis se concentre donc sur la partie spécifique à CristHAL.


*************
Mise en route
*************

On suppose donc que vous disposez d'une machine équipée de Python (version au moins 3.6), et d'un accès 
à un serveur MySQL et à un serveur ElasticSearch. Le code de CristHAL peut être récupéré sur
https://github.com/cedric-cnam/cristhal. Installez-le dans un répertoire que nous appelerons ``cristhaldir``.


.. note:: Dans tout ce qui suit, ``python`` et ``pip`` désignent respectivement les commandes ``python3`` et ``pip3``.
 
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
        }
    }

La configuration d'accès au serveur ElasticSearch est indiquée dans les variables suivantes.
Vous pouvez conserver la valeur de  ``ES_INDEX_REF`` si vous le souhaitez.  Indiquez 
les autres paramètres dans ``ELASTIC_SEARCH``.

.. code-block:: python

      ES_INDEX_REF = "cristhal"
      ELASTIC_SEARCH = {"host": "localhost", "port": 9200, 
                  "index": ES_INDEX_REF}

Pour bien comprendre en quoi ce rôle a des aspects particuliers dans le cadre d'un système distribué à grande
échelle, commençons par la couche matérielle qui va principalement nous occuper dans
ce chapitre.

Un dernier paramètre à régler est l'emplacement des fichiers journaux. Par défaut:

.. code-block:: python

     LOG_DIR = '/var/logs'
    
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

C'est presque prêt! CristHAL propose une autre commande pour créer une configuration initiale.

.. code-block:: bash

     python manage.py init_publis

Quelques messages vous indiquent les opérations effectuées. 

Il ne reste qu'à lancer le serveur intégré à Django.

.. code-block:: bash

     python manage.py runserver

Pas d'erreur ? Alors vous pouvez accèder avec un navigateur quelconque à http://localhost:8000.
Tout est prêt pour commencer à utiliser l'application (en mode 'tests': pour la mise en production
voir ci-dessous).


******************
Mise en production
*******************

