# -*- coding: utf-8 -*-
import os
import sys
import posixpath
import dj_database_url


#SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = '--change-me--'
DEBUG = False

FILER_DEBUG = DEBUG
ALLOWED_HOSTS = ['*',]

# this fixes strange behaviour when running app through gunicorn
DEBUG_TOOLBAR_PATCH_SETTINGS = False


SITE_ID = 1


LOCALE_PATHS = [os.path.join(APP_ROOT, 'locale')]

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
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///app/data.sqlite3')
}


##################################################################
# media, static & co
##################################################################
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(APP_ROOT, 'media'))
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')

STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(APP_ROOT, 'static'))
STATIC_URL = os.getenv('STATIC_URL', '/static/')

ADMIN_MEDIA_PREFIX = os.path.join(APP_ROOT, 'static', 'admin')
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = [
    '/static/'
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OUTPUT_DIR = 'c'



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
# App
##################################################################
PUBLIC_APP_URL = os.getenv('PUBLIC_APP_URL', 'http://127.0.0.1:8000')


##################################################################
# Remote API (OBP)
##################################################################
REMOTE_API_BASE_URL = os.getenv('REMOTE_API_BASE_URL', 'http://dev.openbroadcast.org')
REMOTE_API_USER = os.getenv('REMOTE_API_USER', 'testuser')
REMOTE_API_KEY = os.getenv('REMOTE_API_KEY', 'testkey')


##################################################################
# Fprint index settings
##################################################################
INDEX_BASE_DIR = os.getenv('INDEX_BASE_DIR', os.path.join(MEDIA_ROOT, 'fprint_index'))
