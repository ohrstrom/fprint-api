import dj_database_url

DATABASES['default'] = dj_database_url.config(
    default='postgres://ohrstrom@127.0.0.1:5432/fprint_api_local'
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
