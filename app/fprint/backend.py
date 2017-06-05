import os
import logging
from django.conf import settings

from echoprint_server import query_inverted_index, load_inverted_index, inverted_index_size, decode_echoprint
from echoprint_server_c import _create_index_block
from .models import Entry

INDEX_BASE_DIR = getattr(settings, 'INDEX_BASE_DIR')

log = logging.getLogger(__name__)

class FprintBackend(object):

    index = None
    id_map = []
    index_files = []

    def __init__(self):

        self.index_files = [
            os.path.join(INDEX_BASE_DIR, 'index.bin')
        ]

        # if not self.index:
        #     self.load_index()

    def build_index(self):

        log.info('build index in: {}'.format(INDEX_BASE_DIR))

        if not os.path.isdir(INDEX_BASE_DIR):
            os.makedirs(INDEX_BASE_DIR)

        out_path = os.path.join(INDEX_BASE_DIR, 'index.bin')


        qs = Entry.objects.all().order_by('created')

        batch = parsing_entry_streamer(qs)

        _create_index_block(list(batch), out_path)


        pass


    def load_index(self):

        log.info('load index from: {}'.format(self.index_files))

        self.index = load_inverted_index(self.index_files)
        num_codes_in_index = inverted_index_size(self.index)

        log.debug('index loaded: {}'.format(num_codes_in_index))


        log.info('load id_map')

        self.id_map = [str(e.uuid) for e in Entry.objects.all().order_by('created')]
        num_in_id_map = len(self.id_map)

        log.debug('id_map loaded: {}'.format(num_in_id_map))


        if(num_codes_in_index != num_in_id_map):
            log.error('code / id amount not matching!')




        pass


    def query_index(self, code):

        _, codes = decode_echoprint(str(code))

        results = query_inverted_index(codes, self.index, 'jaccard')

        if self.id_map is not None:
            for r in results:
                r['uuid'] = str(self.id_map[r['index']])

        return results




def parsing_entry_streamer(qs):
    '''
    Convenience generator for converting echoprint strings into codes
    '''
    for entry in qs:
        yield decode_echoprint(
            echoprint_b64_zipped=b'{}'.format(entry.code)
        )[1]
