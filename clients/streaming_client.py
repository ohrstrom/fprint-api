#!/usr/bin/env python
# #-*- coding: utf-8 -*-

# https://github.com/bfirsh/python-echoprint/blob/master/examples/identify.py


import echoprint
import requests
import re
import subprocess
import sys
import struct
import os
import json
import requests
import threading
import time

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class StreamingMonitor(object):

    samples = []

    current_title = None

    def __init__(self, stream_url):

        self.stream_url = stream_url

        meta_thread = threading.Thread(target=self.icy_monitor, args=(self.stream_url,))
        meta_thread.daemon = True
        meta_thread.start()

        stream_thread = threading.Thread(target=self.stream, args=(self.stream_url,))
        stream_thread.daemon = True
        stream_thread.start()


    def stream(self, stream_url):

        stream_url = 'https://www.openbroadcast.org/stream/openbroadcast'

        print('start streaming: {}'.format(stream_url))

        p = subprocess.Popen([
            'ffmpeg',
            '-loglevel',
            'panic',
            '-i', stream_url,
            '-ac', '1',
            '-ar', '11025',
            '-f', 's16le',
            '-',
        ], stdout=subprocess.PIPE)


        while True:
            sample = p.stdout.read(2)
            if not sample == '':
                self.samples.append(struct.unpack('h', sample)[0] / 32768.0)


    def icy_monitor(self, stream_url):

        r = requests.get(stream_url, headers={'Icy-MetaData': '1'}, stream=True)
        if r.encoding is None:
            r.encoding = 'utf-8'

        byte_counter = 0
        meta_counter = 0
        metadata_buffer = StringIO()

        metadata_size = int(r.headers['icy-metaint']) + 255

        data_is_meta = False

        for byte in r.iter_content(1):

            byte_counter += 1

            if (byte_counter <= 2048):
                pass

            if (byte_counter > 2048):
                if (meta_counter == 0):
                    meta_counter += 1

                elif (meta_counter <= int(metadata_size + 1)):

                    metadata_buffer.write(byte)
                    meta_counter += 1
                else:
                    data_is_meta = True

            if (byte_counter > 2048 + metadata_size):
                byte_counter = 0

            if data_is_meta:

                metadata_buffer.seek(0)

                meta = metadata_buffer.read().rstrip(b'\0')

                m = re.search(br"StreamTitle='([^']*)';", str(meta))
                if m:
                    title = m.group(1).decode(r.encoding, errors='replace')
                    print('New title: {}'.format(title))

                    self.current_title = title
                    self.samples = []

                byte_counter = 0
                meta_counter = 0
                metadata_buffer = StringIO()

                data_is_meta = False



if __name__ == '__main__':

    stream = sys.argv[1]

    m = StreamingMonitor(stream)

    while True:

        print('samples in buffer: {}'.format(len(m.samples)))
        time.sleep(1.7)

        if len(m.samples) > 256000:

            d = echoprint.codegen(m.samples)

            data = {
                'code': d['code']
            }

            #FPRINT_API_URL = 'http://172.20.10.240:8000'

            url = 'http://172.20.10.240:8000/api/v1/fprint/identify/'
            r = requests.post(url, json=data)

            results = r.json()

            for res in results[0:3]:
                try:
                    print res['score']
                    print res['uuid'].replace('-', '')
                except:
                    print 'no score'


