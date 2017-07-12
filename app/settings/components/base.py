# -*- coding: utf-8 -*-
import os
import sys
import posixpath


SECRET_KEY = env('SECRET_KEY')

FILER_DEBUG = DEBUG
ALLOWED_HOSTS = ['*',]

# this fixes strange behaviour when running app through gunicorn
DEBUG_TOOLBAR_PATCH_SETTINGS = False

PUBLIC_APP_URL = env('PUBLIC_APP_URL', default='http://127.0.0.1:8000/')
SITE_ID = env.int('SITE_ID', default=1)


LOCALE_PATHS = [root('locale')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


LANGUAGES = [
    ('en', _('English')),
    #('de', _('German')),
]

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'




##################################################################
# applications
##################################################################
INSTALLED_APPS = [

    #'django_slick_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #'django.contrib.sitemaps',
    'django.contrib.humanize',
    #
    'compressor',
    'raven.contrib.django.raven_compat',
    'django_celery_beat',

    # authentication
    'authtools',
    'auth_extra',

    # api
    'api_extra',
    'rest_framework',
    'rest_framework.authtoken',

    # project apps
    'fprint',

]


##################################################################
# middleware
##################################################################
MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##################################################################
# database
##################################################################

##################################################################
# authentication
##################################################################
AUTH_USER_MODEL = 'auth_extra.User'

# TODO: make dynamic
LOGIN_URL = '/account/login/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# LOGIN_REDIRECT_URL = '/account/pick-up/'

##################################################################
# email settings
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



##################################################################
# settings export
##################################################################
SETTINGS_EXPORT = [
    'DEBUG',
    'PUBLIC_APP_URL',
]

##################################################################
# API
##################################################################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

##################################################################
# Remote API (OBP)
##################################################################

REMOTE_API_BASE_URL = env('REMOTE_API_BASE_URL', default='https://www.openbroadcast.org')
REMOTE_API_USER = env('REMOTE_API_USER', default='peter')
REMOTE_API_KEY = env('REMOTE_API_KEY', default='peter')



##################################################################
# Fprint index settings
##################################################################
INDEX_BASE_DIR = env('INDEX_BASE_DIR', default=str(root.path('public/fprint_index/')))
