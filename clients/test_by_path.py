#from __future__ import unicode_literals

import re
import requests
import sys
import os
import json
import subprocess

ECHOPRINT_CODEGEN_BINARY = 'echoprint-codegen'

FPRINT_API_URL = 'http://10.40.10.214:8000'

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

    data = json.loads(p.stdout.read())

    #print(data[0])


    data = {
        'code': data[0]['code']
    }

    print(data)


    url = '{}/api/v1/fprint/identify/'.format(FPRINT_API_URL)

    print(url)

    r = requests.post(url, json=data)

    print(r.text)
    print(r.json())






if __name__ == '__main__':

    path = sys.argv[1]
    test_file(path)


