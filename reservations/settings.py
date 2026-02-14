"""
Django settings for reservations project.
"""
import os
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = 'django-insecure-ik5!h=%np*)@m)j^l1(w9i(!z34d*#&kbbb(rmc8f9gk=skr=6'
DEBUG = True
ALLOWED_HOSTS = []


JAZZMIN_SETTINGS = {
    # Titres
    "site_title": "Réservations PID",
    "site_header": "PID Admin",
    "site_brand": "Gestion Théâtre",
    "welcome_sign": "Bienvenue hicham",
    "copyright": "Projet PID 2026",

    # 1. On vide le menu du haut (Top Menu) pour qu'il soit propre
    "topmenu_links": [],

    # 2. ON FORCE L'AFFICHAGE DANS LA BARRE LATÉRALE (Sidebar)
    # Ils apparaîtront tout en bas de la section "catalogue" à gauche
    "custom_links": {
        "catalogue": [
            {
                "name": "VOIR LE SITE", 
                "url": "/", 
                "icon": "fas fa-eye",
            },
            {
                "name": "DÉCONNEXION", 
                "url": "/accounts/logout/", 
                "icon": "fas fa-sign-out-alt",
            },
        ],
    },

    # 3. Configuration de la barre latérale
    "show_sidebar": True,
    "navigation_expanded": True,

    # 4. Icônes pour faire propre
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "catalogue.Artist": "fas fa-paint-brush",
        "catalogue.Show": "fas fa-theater-masks",
        "catalogue.Reservation": "fas fa-ticket-alt",
        "catalogue.Location": "fas fa-map-marker-alt",
        "catalogue.Locality": "fas fa-map-pin",
    },
    
    # Menu utilisateur (en haut à droite) au cas où tu en as besoin
    "user_menu_links": [
        {"name": "Se déconnecter", "url": "/accounts/logout/", "icon": "fas fa-sign-out-alt"},
    ],
}

# Thème visuel (Flatly est le plus propre)
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
}

# IMPORTANT : Pour que le bouton déconnexion fonctionne sans erreur 405
LOGOUT_ON_GET = True


# Définition des applications
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalogue',          # Ton application principale
    'rest_framework',     # Framework pour l'API
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

ROOT_URLCONF = 'reservations.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Syntaxe moderne et robuste
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

WSGI_APPLICATION = 'reservations.wsgi.application'

# Base de données MariaDB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reservations',
        'USER': 'rooot',
        'PASSWORD': 'rooot',  
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Validation des mots de passe (Configuré selon le document "reste (4)")
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,  # Autorise 6 caractères au lieu de 8
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalisation
LANGUAGE_CODE = 'fr-be'
TIME_ZONE = 'Europe/Brussels'
USE_I18N = True
USE_TZ = True

# Fichiers Statiques et Médias
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de l'API REST (Chapitre 8)
REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [ 
        'rest_framework.authentication.SessionAuthentication', 
        'rest_framework.authentication.BasicAuthentication', 
    ], 
    'DEFAULT_PERMISSION_CLASSES': [ 
        'rest_framework.permissions.IsAuthenticated', 
    ], 
}

# Configuration des redirections (Chapitre 10)
LOGIN_REDIRECT_URL = '/'   # Redirige vers l'accueil après connexion
LOGOUT_REDIRECT_URL = '/'  # Redirige vers l'accueil après déconnexion
LOGIN_URL = 'login'
