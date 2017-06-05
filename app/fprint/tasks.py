from __future__ import absolute_import

import logging

from celery import shared_task
from django.core.files import File

from .renderer import Renderer

log = logging.getLogger(__name__)


@shared_task
def render_entry_task(obj):
    log.debug('Render entry {}'.format(obj.pk))

    r = Renderer()

    try:
        fprint_path = r.render(entry_id=obj.pk, entry_uri=obj.remote_uri)
        with open(fprint_path, 'rb') as f:
            fprint_file = File(f)
            obj.status = obj.STATUS_DONE
            obj.fprint_file.save('fprint.mp3', fprint_file, True)

        log.info('successfully rendered entry id: {}'.format(obj.pk))


    except Exception as e:

        log.error('error rendering entry id: {} - {}'.format(obj.pk, e))
        obj.status = obj.STATUS_ERROR

    # cleans all renderer artefacts
    r.cleanup()

    obj.save()
