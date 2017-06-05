INTERNAL_IPS = (
    '127.0.0.1',
    '10.40.10.40',
)

DEBUG = True

SITE_URL = 'http://j.h612.anorg.net'



TEMPLATES[0]['OPTIONS']['loaders'] = [
    'admin_tools.template_loaders.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
]


##################################################################
# db
##################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'com_example_api_local',
        'USER': 'ohrstrom',
        'HOST': '',
    }
}


##################################################################
# cache
##################################################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
CACHALOT_ENABLED = True
CACHALOT_CACHE = 'cachalot'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': [
#             'localhost:6379',
#         ],
#         'OPTIONS': {
#             'DB': 3,
#         },
#     },
#     'cachalot': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
#
# CACHALOT_CACHE = 'cachalot'
# CACHALOT_ENABLED = True

##################################################################
# queues
##################################################################
CELERY_BROKER_URL = 'redis://localhost:6379/6'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']



##################################################################
# email
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app60734764@heroku.com'
EMAIL_HOST_PASSWORD = 'nsy1yg1v8034'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
# BANDIT_EMAIL = 'jonas@pbi.io'

SENDGRID_EVENTS_IGNORE_MISSING = True




# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/h-email' # change this to a proper location


##################################################################
# media storage on s3
##################################################################

#DEFAULT_FILE_STORAGE = 'project.storage.MediaRootS3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAI7NWURNCBG27YGRQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'com-hoodeenie-local'
AWS_S3_HOST = 's3-eu-west-1.amazonaws.com'
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = {
    'Cache-Control': 'public, max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False



#STATIC_URL = 'https://s3-eu-west-1.amazonaws.com/com-hoodeenie-staging/'
#STATIC_URL = 'https://com-hoodeenie-staging.s3.amazonaws.com/1'
#STATIC_URL = 'https://d2ko6bbh8aq9i.cloudfront.net/'

##################################################################
# staticfiles through whitenose & cloud front
##################################################################




STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 60


#MEDIA_URL = 'http://hoodeenie.j.h612.anorg.net/media/'
#STATIC_URL = 'http://hoodeenie.j.h612.anorg.net/static/'


COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

COMPRESS_OFFLINE_CONTEXT = {
    'template': 'base.html',
}

# cloudfront via "ohrstrom-local"
# d203ybydp8ddao.cloudfront.net

#STATIC_URL = 'https://d203ybydp8ddao.cloudfront.net/static/'

# TURBOLINKS_ENABLED = False

##################################################################
# social auth
##################################################################
SOCIAL_AUTH_USER_MODEL = 'auth_extra.User'
#SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
#SOCIAL_AUTH_FACEBOOK_USERNAME_IS_FULL_EMAIL = True
#SOCIAL_AUTH_FACEBOOK_USER_FIELDS = ['email',]

#SOCIAL_AUTH_EMAIL_FORM_URL = '/account/login/'
SOCIAL_AUTH_EMAIL_FORM_URL = 'auth_extra:login'


SOCIAL_AUTH_GITHUB_KEY = '5a64351c4a24e4f4ac96'
SOCIAL_AUTH_GITHUB_SECRET = '89f22f62dad16d5d7f0fc60b41de4a54bd5a8899'
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email',]

SOCIAL_AUTH_FACEBOOK_KEY = '345836865799707'
SOCIAL_AUTH_FACEBOOK_SECRET = '01dcd5c5652a85d185c906f9fd9637b7'
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_about_me', 'user_hometown']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile',]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '184969603265-3dv9gd04tjvp8sqcn3cl6m0fncrubq5i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'nnI2qHwi6KfT_C4LcSrKzeTR'


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
    #'devserver',
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'devserver.middleware.DevServerMiddleware',
    #'base.middleware.profile.ProfileMiddleware',
]

DEBUG_TOOLBAR_PANELS = [

]

WERKZEUG_DEBUG_PIN = 'off'


#DEVSERVER_IGNORED_PREFIXES = ['/media', '/static']

DEVSERVER_MODULES = (
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)



from colorlog import ColoredFormatter
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(lineno)-4s [%(levelname)s] %(name)s: %(message)s'
        },
        'debug': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'bold_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {

        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console',],
            'propagate': False
        },
        '': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'matching': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'notification': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'flatshare': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'dev': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


# MATCHING_SKIP_UPDATE = True
MATCHING_ALWAYS_UPDATE = True
MATCHING_RUN_ASYNC = False


EL_PAGINATION_PER_PAGE = 24

PLACEHOLDER_IMAGE_DEFAULT_COLOR = '#333333'


SENDGRID_EVENTS_IGNORE_MISSING = True
NOTIFICATION_EMAIL_RUN_ASYNC = False


LOADERIO_TOKEN = '1fbbd921ffd3a8bcee22d45909db83c0'
