"""
Django settings for CristHal project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#
# Stockage des fichiers, comme les CSV des sources par exemple
# Il est sans doute préférable de le placer hors de l'arborescence cristhal
#

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Configuration de test: en production, redéfinir ces valeurs dans local_settings.py
DEBUG = True
SECRET_KEY='à_protéger_impérativement'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        'crispy_forms',
    'accueil',
    'publis'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cristhal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

WSGI_APPLICATION = 'cristhal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'NAME': 'cristhal',
        'USER': 'cristhalAdmin',
        'PASSWORD': 'mdpCristhal',
        'HOST': '127.0.0.1',
        'PORT': '3306',
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
# Configuration du journal
#
LOGGER_NAME="cristhal"
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {filename} - line {lineno}:  {message} ',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
         
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'cristhal.log') ,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT=''
STATIC_URL =  "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

#
# Répertoire pour les fichiers exportés. Par défaut dans 'media'.
# Attention aux droits d'accès: cristhal essaiera de la créer s'il n'existe pas
#

EXPORT_DIR = os.path.join(MEDIA_ROOT, 'export')

# Nom de l'index pour le référentiel des publis
ES_INDEX_REF = "cristhal"


# Nouveau Django 3.2: type des clés primaires
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# 
# Paramétrage ElasticSearch
#
ELASTIC_SEARCH = {"host": "localhost", "port": 9200, "index": ES_INDEX_REF}

# Le paramétrage spécifique à un site doit être placé dans un fichier local_settings.py
try:
    from cristhal.local_settings import *
    print("Prise en compte de la configuration dans le fichier local_settings.py")
except ImportError as error:
    print("Pas de fichier 'local_settings.py', donc pas de configuration locale. Normal?")


