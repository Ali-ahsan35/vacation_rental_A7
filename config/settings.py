"""
Django settings for vacation rental project.

WHAT THIS FILE DOES:
- Configures database connection
- Lists all installed apps
- Sets up templates and static files
- Configures media files (uploaded images)
- Sets up REST framework for API
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# EXPLANATION: BASE_DIR is the root folder of your project


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'
# EXPLANATION: This key is used for security. Change it in production!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# EXPLANATION: DEBUG=True shows detailed errors. Set to False in production.

ALLOWED_HOSTS = []
# EXPLANATION: Which domains can access this site. Empty = only localhost


# Application definition
# EXPLANATION: These are all the apps Django will use

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',        
    'django.contrib.auth',         
    'django.contrib.contenttypes', 
    'django.contrib.sessions',     
    'django.contrib.messages',     
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',              
    'django_filters',             
    
    # Our custom apps
    'locations',                   # Location model
    'properties',                  # Property model  
    'images',                      # PropertyImage model
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
# Middleware processes every request/response

ROOT_URLCONF = 'config.urls'
# Points to the main URL configuration file


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Our templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # For media files
            ],
        },
    },
]
# Tells Django where to find HTML templates

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Media files (User uploaded files - property images!)
# where uploaded property images will be stored
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST Framework settings
# Configuration for API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Show 10 items per page
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}