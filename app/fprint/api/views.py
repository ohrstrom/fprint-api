# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.db.utils import ProgrammingError

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import EntrySerializer
from ..models import Entry

from ..backend import FprintBackend


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


    # search / identify handling
    def identify(self, request, *args, **kwargs):

        data = request.data

        code = data['code']

        # a bit ugly...
        if not backend.index:
            backend.load_index()

        results = backend.query_index(code=code)

        for r in results:
            r['uri'] = reverse('api:fprint-api:entry-detail', kwargs={'uuid': r['uuid']})


        return Response(results, status=status.HTTP_200_OK)




entry_list = EntryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

entry_detail = EntryViewSet.as_view({
    'get': 'retrieve',
    'put': 'get_or_create_detail',
    'patch': 'update',
})

entry_identify = EntryViewSet.as_view({
    'post': 'identify',
})



#######################################################################
# control views
#######################################################################

@api_view(['GET',])
def reload_index(request):
    backend.load_index()

    return Response({"num_ids": len(backend.id_map)})


