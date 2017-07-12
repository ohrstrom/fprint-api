# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import Entry
from ..remote import APIClient, API_BASE_URL



class EntrySerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:fprint-api:entry-detail',
        lookup_field='uuid'
    )


    uuid = serializers.UUIDField(
        required=True,
        validators=[UniqueValidator(queryset=Entry.objects.all())]
    )


    code = serializers.CharField(
        allow_blank=False,
        write_only=True
    )

    index_id = serializers.IntegerField(
        read_only=True
    )

    status_display = serializers.SerializerMethodField()
    def get_status_display(self, obj):
        return '{}'.format(obj.get_status_display())


    class Meta:
        model = Entry
        depth = 1
        fields = [
            'url',
            'uuid',
            'status',
            'status_display',
            'code',
            'index_id',
            'name',
            'artist_name',
            'duration',
        ]
        # extra_kwargs = {
        #         'code': {'write_only': True}
        # }
