##################################################################
# debug settings
##################################################################
INTERNAL_IPS = (
    '127.0.0.1',
)
DEBUG = True
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
TURBOLINKS_ENABLED = False


##################################################################
# database
##################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'com_hoodeenie_local',
        'USER': 'hoodeenie',
        'PASSWORD': 'hoodeenie',
    }
}

##################################################################
# cache
##################################################################
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
# }


##################################################################
# social auth
# see also AUTHENTICATION_BACKENDS
##################################################################
SOCIAL_AUTH_USER_MODEL = 'auth_extra.User'
SOCIAL_AUTH_EMAIL_FORM_URL = 'auth_extra:login'

SOCIAL_AUTH_GITHUB_KEY = '***'
SOCIAL_AUTH_GITHUB_SECRET = '***'
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email',]

SOCIAL_AUTH_FACEBOOK_KEY = '***'
SOCIAL_AUTH_FACEBOOK_SECRET = '***'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile',]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

WERKZEUG_DEBUG_PIN = 'off'
