from __future__ import absolute_import

import logging

from celery import shared_task
from django.core.files import File

log = logging.getLogger(__name__)


# @shared_task
# def process_entry_task(obj):
#     log.debug('Process entry {}'.format(obj.pk))

