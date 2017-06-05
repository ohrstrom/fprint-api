# Microservice / API Blueprint

Work In Progress...

 - [Documentation](docs/index.md)



### Run devserver

    fprint-api runserver 0.0.0.0:8080



### Run as uWSGI Service

    uwsgi --http :8080 --module app.wsgi --virtualenv ~/srv/fprint-api
