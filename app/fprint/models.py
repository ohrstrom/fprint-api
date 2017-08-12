# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


log = logging.getLogger(__name__)

RUN_ASYNC = True

# number of codes to be stored per index
CODES_PER_INDEX = 1024

class Entry(models.Model):

    STATUS_INIT = 0
    STATUS_PENDING = 1
    STATUS_DONE = 2
    STATUS_DELETED = 90
    STATUS_ERROR = 99

    STATUS_CHOICES = (
        (STATUS_INIT, 'Initialized'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_DONE, 'Done'),
        (STATUS_DELETED, 'Deleted'),
        (STATUS_ERROR, 'Error'),
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

    # identification fields
    code = models.TextField(
        null=True, blank=False,
        help_text=_('Echoprint code string, compressed')
    )

    duration = models.DurationField(
        null=True, blank=False, db_index=True,
        help_text=_('Duration in seconds (float)')
    )

    name = models.CharField(
        _('Track Name/Title'),
        null=True, blank=True, max_length=(256), db_index=True,
        help_text=_('Normalised to ASCII')
    )

    artist_name = models.CharField(
        _('Artist Name'),
        null=True, blank=True, max_length=(256), db_index=True,
        help_text=_('Normalised to ASCII')
    )

    index_id = models.PositiveIntegerField(
        null=True, blank=False
    )

    class Meta:
        ordering = ['pk']


@receiver(pre_save, sender=Entry)
def entry_pre_save(sender, instance, **kwargs):

    # check for changes
    if instance.pk:
        _old_instance = Entry.objects.get(pk=instance.pk)

        if instance.code != _old_instance.code:
            instance.status = Entry.STATUS_PENDING
            log.debug('code changed for {}'.format(instance.uuid))



@receiver(post_save, sender=Entry)
def entry_post_save(sender, instance, **kwargs):

    # calculate index id
    # increase index id every CODES_PER_INDEX block
    index_id = (instance.pk - 1) / CODES_PER_INDEX + 1
    if instance.index_id != index_id:
        # log.debug('setting index id for {} to {}'.format(instance.pk, index_id))
        Entry.objects.filter(pk=instance.pk).update(index_id=index_id)
        instance.refresh_from_db()


    if instance.status < Entry.STATUS_DONE:
        # log.debug('Entry {} needs processing'.format(instance.pk))
        if RUN_ASYNC:
            pass
        else:
            pass
