# Echoprint API Service

## Overview

`fprint-api` is a [Django](https://www.djangoproject.com/) based web-service built on top of 
[echoprint-server](https://github.com/spotify/echoprint-server) (Initially developped by Echonest, later acquired by
[Spotify](https://github.com/spotify/)).

`fprint-api` uses the C-based [libechoprintserver.c](https://github.com/spotify/echoprint-server/blob/master/libechoprintserver.c)
and provides the components to ingest and query fingerprint *codes* to/from the *index* as well as (re-)building the 
index data - and provides an API built using [Django REST framework](http://www.django-rest-framework.org/).


## Installation

### From Source

((t.b.d.))


### Using PIP

((t.b.d.))







### Run devserver

    fprint-api runserver 0.0.0.0:8080



### Run as uWSGI Service

    uwsgi --http :8080 --module app.wsgi --virtualenv ~/srv/fprint-api

