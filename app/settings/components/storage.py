# -*- coding: utf-8 -*-
import os




##################################################################
# Fprint index settings
##################################################################
INDEX_BASE_DIR = os.getenv('INDEX_BASE_DIR', os.path.join(MEDIA_ROOT, 'fprint_index'))




# CACHES = {
#     'default': env.cache(),
#     #'redis': env.cache('REDIS_URL')
# }
#
# CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379') + '/6'
# CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379') + '/6'
# CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_ACCEPT_CONTENT = ['json', 'pickle']
# #CELERYD_CHDIR = "/app/website"
