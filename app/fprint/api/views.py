# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.urls import reverse
from django.db.utils import ProgrammingError
from django.conf import settings
from django.db.models import Q, Case, When

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from datetime import timedelta

from .serializers import EntrySerializer
from ..models import Entry

from ..backend import FprintBackend

RESULT_MIN_SCORE = 0.011 # score-range: 0 - 1
RESULT_DURATION_TOLERANCE = 10.0 # seconds

PUBLIC_APP_URL = getattr(settings, 'PUBLIC_APP_URL')

log = logging.getLogger(__name__)

backend = FprintBackend()


try:
    backend.load_index()
except ProgrammingError as e:
    # database not ready/migrated
    # TODO: check for a better way to handle this case
    pass


class EntryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Entry.objects.all().order_by('-created')
    serializer_class = EntrySerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):

        queryset = Entry.objects.filter().order_by('-created')
        page = self.paginate_queryset(queryset)

        serializer = EntrySerializer(
            page,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_or_create_detail(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            print(e)

        data = request.data
        data.update({
            'uuid': kwargs.get('uuid')
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.status = Entry.STATUS_DELETED
        instance.save()

    # search / identify handling
    def identify(self, request, *args, **kwargs):
        """
        identify entry by 'code' / fingerprint
        accepts `echoprint-codegen` (version 4.12) generated format. 
        used out of the code is the following information:
        
            {
                'code': '<encoded code>',
                'metadata': {
                    'duration': '<duration in seconds>',
                }
            }
            
        """

        data = request.data

        code = data['code']
        min_score = data.get('min_score', RESULT_MIN_SCORE)
        duration_tolerance = data.get('duration_tolerance', RESULT_DURATION_TOLERANCE)
        metadata = data.get('metadata', {})
        duration = metadata.get('duration')

        # a bit ugly...
        if not backend.index:
            backend.load_index()

        _results = backend.query_index(code=code)

        # remove results with score below threshold
        results = list(filter(lambda d: d['score'] > min_score, _results))

        # created sorted queryset out of results
        uuid_list = [r['uuid'] for r in results]
        preserved = Case(*[When(uuid=uuid, then=pos) for pos, uuid in enumerate(uuid_list)])
        qs = Entry.objects.filter(uuid__in=uuid_list).order_by(preserved).distinct()


        if duration:

            duration_min = timedelta(seconds=float(duration) - float(duration_tolerance))
            duration_max = timedelta(seconds=float(duration) + float(duration_tolerance))

            # print('duration_tolerance: {}'.format(duration_tolerance))
            # print('duration_min:       {}'.format(duration_min))
            # print('duration_max:       {}'.format(duration_max))

            log.debug('filter by duration - tolerance: {} - min: {} - max: {}'.format(
                duration_tolerance,
                duration_min,
                duration_max,
            ))

            qs = qs.filter(duration__range=[duration_min, duration_max])

        data = []


        for entry in qs:

            # get original dict from results
            # https://stackoverflow.com/a/8653568/469111
            _r = (item for item in results if item['uuid'] == str(entry.uuid)).next()

            data.append({
                'uuid': '{}'.format(entry.uuid),
                'duration': '{}'.format(float(entry.duration.seconds)),
                'name': '{}'.format(entry.name),
                'artist': '{}'.format(entry.artist_name),
                #'uri': '{}{}'.format(PUBLIC_APP_URL, reverse('api:fprint-api:entry-detail', kwargs={'uuid': entry.uuid})),
                'score': '{}'.format(_r['score']),
            })



        num_results = len(data)

        if num_results:
            log.debug('highest score: {} - num. results: {} - min. score: {}'.format(data[0]['score'], num_results, min_score))
        else:
            log.debug('no results for code')




        # for r in results:
        #     r['uri'] = '{}{}'.format(PUBLIC_APP_URL, reverse('api:fprint-api:entry-detail', kwargs={'uuid': r['uuid']}))



        return Response(data, status=status.HTTP_200_OK)




entry_list = EntryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

entry_detail = EntryViewSet.as_view({
    'get': 'retrieve',
    'put': 'get_or_create_detail',
    'patch': 'update',
    'delete': 'destroy',
})

entry_identify = EntryViewSet.as_view({
    'post': 'identify',
})



#######################################################################
# control views
#######################################################################

@api_view(['GET',])
def build_index(request):
    """
    view to trigger index-rebuilding from 'outside'.
    """
    backend.build_index()

    return Response({"num_ids": len(backend.id_map)})

@api_view(['GET',])
def reload_index(request):
    """
    view to trigger index-reloading from 'outside'.
    needed e.g. for the `fprint_cli update_index` command.
    """
    backend.load_index()

    return Response({"num_ids": len(backend.id_map)})


