from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    list_display = [
        'uuid',
        'index_id',
        'created',
        'updated',
        'status',
    ]

    list_filter= [
        'status',
        'index_id',
    ]


    pass
