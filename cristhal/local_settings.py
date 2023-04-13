"""
 Exemple d'un fichier local_settings.py contenant 
 les spécificités d'une configuration locale
 
  Toutes les valeurs définies ici remplacent celles du fichier settings.py
  
 Pour un déploiement en production: voir la documentation Django, par exempple
  https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

"""
import os

from .settings import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# Clé secrète, À prendre dans une variable d'environnement ou un fichier
#
#SECRET_KEY = os.environ['SECRET_KEY']

#
# Indiquer les domaines servis par l'app.
#
ALLOWED_HOSTS = []
#
# Très important: pas de DEBUG en production
#
#DEBUG=False
#

# Connexion à la base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cristhal',
        'USER': 'cristhalAdmin',
        'PASSWORD': 'mdpCristhal',
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


#
# Messages
#
EMAIL_BACKEND='philippe.rigaux@cnam.fr'


# Pour les fichiers d'export. Le serveur doit pouvoir y écrire
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Exemple: pour écrire dans un répertoire logs frère du répertoire courant
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

#
# Fichiers de log. P
#
LOG_DIR = '/var/log'
#
# Exemple: pour écrire dans un répertoire logs frère du répertoire courant
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')

# Ne pas toucher cette ligne
LOGGING["handlers"]["file"]["filename"] = os.path.join(LOG_DIR, 'cristhal.log')

# 
# Configuration ElasticSearch
#
ES_INDEX_REF = "cristhal"

ES_INDEX_REF = "cristhal"
ELASTIC_SEARCH = {"host": "localhost", "port": 9200, 
                  "index": ES_INDEX_REF,
                  "auth_login": "elastic",
                   "auth_password": "2C6gjm7sTtD5J0hOyOdn"
                  }

