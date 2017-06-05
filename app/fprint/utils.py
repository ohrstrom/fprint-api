#-*- coding: utf-8 -*-

#from __future__ import unicode_literals

import os
from django.conf import settings

from echoprint_server import load_inverted_index, create_inverted_index,  parsed_code_streamer, parsing_code_streamer
from echoprint_server.lib import decode_echoprint
from echoprint_server_c import _create_index_block


INDEX_BASE_DIR = getattr(settings, 'INDEX_BASE_DIR')


def build_index(queryset):

    if not os.path.isdir(INDEX_BASE_DIR):
        os.makedirs(INDEX_BASE_DIR)

    out_path = os.path.join(INDEX_BASE_DIR, 'index.bin')
    batch = parsing_entry_streamer(queryset)

    _create_index_block(list(batch), out_path)

    # for entry in queryset:
    #
    #     #print(entry.code)
    #
    #     offsets, codes = decode_echoprint(b'{}'.format(entry.code))
    #
    #     print '********'
    #     print offsets
    #     print codes
    #     print
    #
    # pass


def build_index_block():

    pass



def parsing_entry_streamer(qs):
    '''
    Convenience generator for converting echoprint strings into codes
    '''
    for entry in qs:
        yield decode_echoprint(
            echoprint_b64_zipped=b'{}'.format(entry.code)
        )[1]


