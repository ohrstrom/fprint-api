# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    save_on_top = True

    date_hierarchy = 'created'

    list_display = [
        'uuid',
        'duration',
        'name',
        'artist_name',
        'index_id',
        'created',
        'updated',
        'status',
    ]

    list_filter= [
        'status',
        'index_id',
        'created',
        'updated',
    ]

    search_fields = [
        'uuid',
        'name',
        'artist_name',
    ]
