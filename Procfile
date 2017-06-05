web: uwsgi --http :$PORT --module app.wsgi
queue: celery -A app worker -l info
