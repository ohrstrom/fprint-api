#from __future__ import unicode_literals

import re
import requests
import sys
import os
import json
import subprocess

ECHOPRINT_CODEGEN_BINARY = 'echoprint-codegen'

FPRINT_API_URL = 'http://10.40.10.214:8000'
#FPRINT_API_URL = 'http://172.20.10.240:8000'
#FPRINT_API_URL = 'http://127.0.0.1:7777'

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

def test_file(path):

    path = os.path.abspath(path)

    print(path)

    command = [
        ECHOPRINT_CODEGEN_BINARY,
        path
    ]

    p = subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)

    data = json.loads(p.stdout.read())[0]

    # print('***********************')
    # print(data)
    # print('***********************')


    # data = {
    #     'code': data['code']
    # }

    data.update({
            'min_score': 0.10,
            'duration_tolerance': 1.5,
        })


    url = '{}/api/v1/fprint/identify/'.format(FPRINT_API_URL)

    print(url)

    r = requests.post(url, json=data)

    results = r.json()

    for result in results:
        print(result)

        # r2 = requests.get('http://local.openbroadcast.org:8080/api/v1/library/track/{}/'.format(result['uuid']))
        # print(r2.json())
        print('-----------------------------')

        #print('http://local.openbroadcast.org:8080/api/v1/library/track/{}/?format=json'.format(result['uuid']))



if __name__ == '__main__':

    path = sys.argv[1]
    test_file(path)
