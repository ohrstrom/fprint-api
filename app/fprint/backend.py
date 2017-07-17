import os
import logging
import time
import requests
from django.conf import settings

from echoprint_server import query_inverted_index, load_inverted_index, inverted_index_size, decode_echoprint
from echoprint_server_c import _create_index_block
from .models import Entry

INDEX_BASE_DIR = getattr(settings, 'INDEX_BASE_DIR')
PUBLIC_APP_URL = getattr(settings, 'PUBLIC_APP_URL')

log = logging.getLogger(__name__)

class FprintBackend(object):

    index = None
    id_map = []


    def __init__(self):
        pass


    def build_index(self, force_rebuild=False):

        log.info('build index in: {}'.format(INDEX_BASE_DIR))

        if not os.path.isdir(INDEX_BASE_DIR):
            os.makedirs(INDEX_BASE_DIR)


        # slice queryset by index id
        # get used index ids
        index_ids = [e[0] for e in Entry.objects.order_by('index_id').distinct('index_id').values_list('index_id')]

        log.info('got {} index sequences'.format(len(index_ids)))

        for index_id in index_ids:

            # chek for each index block if there are entries that need to be updated.
            # only a whole block can be updated as a whole

            qs = Entry.objects.filter(index_id=index_id)
            pending_count = qs.filter(status=Entry.STATUS_PENDING).count()

            index_file = os.path.join(INDEX_BASE_DIR, 'index_{:06d}.bin'.format(index_id))

            print('{} pending entries for index {}'.format(pending_count, index_id))

            if force_rebuild or pending_count > 0:

                log.debug('{} pending entries for index {}'.format(pending_count, index_id))

                start_time = time.time()

                batch = parsing_entry_streamer(qs)
                _create_index_block(list(batch), index_file)

                duration = (time.time() - start_time)
                log.debug('rebuilt index in: {}'.format(duration))
                print('rebuilt index in: {}'.format(duration))

                qs.update(status=Entry.STATUS_DONE)

        # TODO: implement propperly
        # notify API to reload index data
        url = '{}/api/v1/fprint/controls/reload-index/'.format(PUBLIC_APP_URL)
        r = requests.get(url)




    def load_index(self):

        num_codes_in_index = 0
        num_in_id_map = 0


        index_files = []
        index_ids = [e[0] for e in Entry.objects.order_by('index_id').distinct('index_id').values_list('index_id')]

        for index_id in index_ids:
            index_file = os.path.join(INDEX_BASE_DIR, 'index_{:06d}.bin'.format(index_id))
            index_files.append(index_file)


        try:

            start_time = time.time()

            self.index = load_inverted_index(index_files)
            num_codes_in_index = inverted_index_size(self.index)

            duration = (time.time() - start_time)

            log.debug('index loaded: {} entries in {} s'.format(num_codes_in_index, duration))
        except Exception as e:
            log.warning('unable to load index: {}'.format(e))



        try:

            start_time = time.time()

            self.id_map = [str(e[0]) for e in Entry.objects.values_list('uuid')]

            num_in_id_map = len(self.id_map)

            duration = (time.time() - start_time)

            log.debug('id_map loaded: {} entries in {} s'.format(num_in_id_map, duration))


        except Exception as e:
            log.warning('unable to load id_map: {}'.format(e))


        if(num_codes_in_index != num_in_id_map):
            log.error('code / id amount not matching! codes: {} vs ids: {}'.format(num_codes_in_index, num_in_id_map))



    def query_index(self, code):

        if not self.index:
            log.info('query_index: index ot loaded > load it')
            self.load_index()

        _, codes = decode_echoprint(str(code))

        results = query_inverted_index(codes, self.index, 'jaccard')

        if self.id_map is not None:
            for r in results:
                r['uuid'] = str(self.id_map[r['index']])

        return results




def parsing_entry_streamer(qs):

    for entry in qs:

        yield decode_echoprint(
            echoprint_b64_zipped=b'{}'.format(entry.code)
        )[1]
