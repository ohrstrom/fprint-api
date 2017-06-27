# -*- coding: utf-8 -*-
import os
import sys
import environ
from split_settings.tools import optional, include

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
env.read_env('.env')
SITE_ROOT = root()
DEBUG = env('DEBUG')

# add app path
sys.path.insert(0, SITE_ROOT)

#
gettext = lambda s: s
_ = gettext

# dev & test
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

include(
    'components/base.py',
    'components/template.py',
    'components/storage.py',
    scope=locals()
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s %(lineno)-4s [%(levelname)s] %(name)s: %(message)s'
#         },
#         'debug': {
#             'format': '[%(levelname)s] %(name)s: %(message)s'
#         },
#         'colored': {
#             '()': 'colorlog.ColoredFormatter',
#             'format': '%(log_color)s%(asctime)s %(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
#             'log_colors': {
#                 'DEBUG': 'cyan',
#                 'INFO': 'bold_green',
#                 'WARNING': 'yellow',
#                 'ERROR': 'red',
#                 'CRITICAL': 'bold_red',
#             },
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'colored',
#         },
#     },
#     'loggers': {
#
#         'django.db.backends': {
#             'level': 'ERROR',
#             'handlers': ['console',],
#             'propagate': False
#         },
#         '': {
#             'handlers': ['console',],
#             'level': 'ERROR',
#             'propagate': False
#         },
#         'django.request': {
#             'handlers': ['console'],
#             'level': 'ERROR',
#             'propagate': False
#         },
#         'celery': {
#             'handlers': ['console'],
#             'level': 'WARNING',
#             'propagate': False
#         },
#         'dev': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         'echoprint_server': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         'fprint': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#     }
# }
