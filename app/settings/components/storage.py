

MEDIA_ROOT = env('MEDIA_ROOT', default=str(root.path('public/media/')))
MEDIA_URL = env('MEDIA_URL', default='/media/')

STATIC_ROOT = env('STATIC_ROOT', default=str(root.path('public/static/')))
STATIC_URL = env('STATIC_URL', default='/static/')


ADMIN_MEDIA_PREFIX = root.path('static/admin/')
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




DATABASES = {
    'default': env.db(),
}

CACHES = {
    'default': env.cache(),
    #'redis': env.cache('REDIS_URL')
}

CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379') + '/6'
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379') + '/6'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
#CELERYD_CHDIR = "/app/website"
