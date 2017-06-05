import requests

from django.conf import settings

API_BASE_URL = getattr(settings, 'REMOTE_API_BASE_URL')
API_USER = getattr(settings, 'REMOTE_API_USER')
API_KEY = getattr(settings, 'REMOTE_API_KEY')

REQUEST_HEADERS = {
    'User-Agent': 'Fprint Agent 0.0.1',
    'Authorization': 'ApiKey {api_user}:{api_key}'.format(
        api_user=API_USER,
        api_key=API_KEY
    )
}

class APIClient(object):
    def get(self, url, *args, **kwargs):
        kwargs['headers'] = REQUEST_HEADERS
        return requests.get(url, *args, **kwargs)
