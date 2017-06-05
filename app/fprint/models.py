# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .remote import APIClient
from .tasks import render_entry_task

log = logging.getLogger(__name__)

RUN_ASYNC = True

CODES_PER_INDEX = 65535


class Entry(models.Model):
    STATUS_INIT = 0
    STATUS_PENDING = 1
    STATUS_DONE = 2
    STATUS_ERROR = 99

    STATUS_CHOICES = (
        (STATUS_INIT, _('Initialized')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_DONE, _('Done')),
        (STATUS_ERROR, _('Error')),
    )

    status = models.PositiveSmallIntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        blank=False, null=False,
        db_index=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=True, db_index=True, unique=True,
        help_text=_('The UUID is is set from "outside"/client when ingesting a fingerprint')
    )

    created = models.DateTimeField(
        auto_now_add=True, editable=False, db_index=True
    )

    updated = models.DateTimeField(
        auto_now=True, editable=False, db_index=True
    )

    code = models.TextField(
        null=True, blank=False
    )

    index_id = models.PositiveIntegerField(
        null=True, blank=False
    )


@receiver(pre_save, sender=Entry)
def entry_pre_save(sender, instance, **kwargs):
    # calculate index id
    # increase index id every CODES_PER_INDEX block
    num_entries = Entry.objects.all().count()
    if num_entries < 1:
        instance.index_id = 1
    else:
        instance.index_id = (num_entries - 1) / CODES_PER_INDEX + 1


        # if not instance.pk:
        #     log.debug('Object creation.')


@receiver(post_save, sender=Entry)
def entry_post_save(sender, instance, **kwargs):
    if instance.status < Entry.STATUS_DONE:
        log.debug('Entry {} needs processing'.format(instance.pk))

        if RUN_ASYNC:
            pass
            # render_entry_task.apply_async((instance,))
        else:
            pass
            # render_entry_task(instance)



