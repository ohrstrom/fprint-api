# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

app_name = 'fprint-api'
urlpatterns = [
    # entry urls
    url(r'^identify/$', views.entry_identify, name='entry-identify'),
    url(r'^entry/$', views.entry_list, name='entry-list'),
    url(r'^entry/(?P<uuid>[0-9A-Fa-f-]+)/$', views.entry_detail, name='entry-detail'),

    # control urls
    url(r'^controls/reload-index/$', views.reload_index, name='controls-reload-index'),
]
