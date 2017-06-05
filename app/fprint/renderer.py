# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import shutil
import subprocess
import tempfile



from .remote import APIClient, API_BASE_URL

log = logging.getLogger(__name__)


#######################################################################
# handle cue/fade for single media/item
# needs to be top level function, else it cannot be pickled
# for Pool
#######################################################################
def process_part(media):
    log.debug('fades: {fade_in} - {fade_out} : cues: {cue_in} {cue_out}'.format(
        fade_in=media['fade_in'],
        fade_out=media['fade_out'],
        cue_in=media['cue_in'],
        cue_out=media['cue_out'],
    ))

    tfm = sox.Transformer()

    if (media['cue_in'] + media['cue_out']) > 0.0:
        tfm.trim(media['cue_in'], media['cue_out'])

    if (media['fade_in'] + media['fade_out']) > 0.0:
        tfm.fade(fade_in_len=media['fade_in'], fade_out_len=media['fade_out'])

    tfm.build(media['in_file_path'], media['part_file_path'])

    return


#######################################################################
# handle file downloading
# needs to be top level function, else it cannot be pickled
# for Pool
#######################################################################
def download_file(uri, path):
    log.debug('downloading {} to {}'.format(uri, path))

    r = APIClient().get(uri, stream=True)

    if r.status_code == 200:

        log.debug('status: {} path: {}'.format(r.status_code, path))

        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    return r.status_code


#######################################################################
# Entry Renderer
#######################################################################
class Renderer(object):
    entry_data = None
    output_path = None
    lock = None

    def __init__(self):
        self.api_client = APIClient()
        pass

    def prepare(self, uri, id):

        self.id = id

        ###############################################################
        # set working dir
        ###############################################################
        # self.working_dir = os.path.join(os.getcwd(), 'data', str(id))
        self.working_dir = tempfile.mkdtemp()

        ###############################################################
        # define output files
        ###############################################################
        self.output_path = os.path.join(self.working_dir, 'combined.mp3')
        self.meta_path = os.path.join(self.working_dir, 'meta.json')

        ###############################################################
        # create working dir & lock
        ###############################################################
        if not os.path.isdir(self.working_dir):
            os.makedirs(self.working_dir)

        ###############################################################
        # get entry from api
        ###############################################################
        log.info('download entry: {}'.format(uri))

        r = self.api_client.get(uri, params={'all': 'yes'})

        if not r.status_code == 200:
            raise Exception(r.status_code)

        data = r.json()

        ###############################################################
        # create directories
        ###############################################################

        in_dir = os.path.join(self.working_dir, 'in')
        parts_dir = os.path.join(self.working_dir, 'parts')
        out_dir = os.path.join(self.working_dir, 'out')

        for d in [in_dir, parts_dir, out_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        self.in_dir = in_dir
        self.parts_dir = parts_dir
        self.out_dir = out_dir

        ###############################################################
        # map data
        ###############################################################
        entry_data = {
            'uuid': data['uuid'],
            'media': [],
        }
        for media in data['items']:
            in_file_uri = '{base_url}{path}stream.mp3'.format(
                base_url=API_BASE_URL,
                path=media['item']['resource_uri']
            )

            in_file_path = os.path.join(self.in_dir, '{}.mp3'.format(media['item']['uuid']))
            part_file_path = os.path.join(self.parts_dir, '{}.mp3'.format(media['item']['uuid']))

            entry_data['media'].append({
                'skip_processing': (int(media['cue_in']) + int(media['cue_out']) + int(media['fade_in']) + int(
                    media['fade_out'])) <= 0,
                'cue_in': float(media['cue_in']) / 1000.0,
                # 'cue_out': float(media['cue_out']) / 1000.0,
                'cue_out': (float(media['item']['content_object']['duration']) - float(media['cue_out'])) / 1000.0,
                'fade_in': float(media['fade_in']) / 1000.0,
                'fade_out': float(media['fade_out']) / 1000.0,
                'in_file_uri': in_file_uri,
                'in_file_path': in_file_path,
                'part_file_path': part_file_path,
            })

        print('*' * 72)
        print()
        print('*' * 72)

        self.entry_data = entry_data

        return entry_data

    ###################################################################
    # download source files from api
    ###################################################################
    def download_media(self):

        # hm - celery does not allow multiprocessing:
        # "daemonic processes are not allowed to have children"
        # so non-async version for the moment

        for media in self.entry_data['media']:
            log.debug('queueing file for download: {}'.format(media['in_file_uri']))
            url = media['in_file_uri']
            path = media['in_file_path']
            download_file(url, path)

        return

        # pool = Pool()
        #
        # procs = []
        #
        # for media in self.entry_data['media']:
        #
        #     log.debug('queueing file for download: {}'.format(media['in_file_uri']))
        #
        #     url = media['in_file_uri']
        #     path = media['in_file_path']
        #
        #     procs.append(pool.apply_async(download_file, args=(url, path)))
        #
        # #[p.get() for p in procs]
        #
        # pool.close()
        # pool.join()
        #
        # log.info('completed downloading files')
        #
        # return

    ###################################################################
    # cue & fade parts
    ###################################################################
    def process_parts(self):

        # hm - celery does not allow multiprocessing:
        # "daemonic processes are not allowed to have children"
        # so non-async version for the moment

        for media in self.entry_data['media']:

            if media['skip_processing']:
                log.debug('no processing needed: {}'.format(media['in_file_path']))
                shutil.copyfile(media['in_file_path'], media['part_file_path'])
            else:
                process_part(media)

        return

        # pool = Pool()
        #
        # procs = []
        #
        # for media in self.entry_data['media']:
        #
        #     if media['skip_processing']:
        #         log.debug('no processing needed: {}'.format(media['in_file_path']))
        #         shutil.copyfile(media['in_file_path'] , media['part_file_path'])
        #     else:
        #         procs.append(pool.apply_async(process_part, args=(media,)))
        #
        # #[p.get() for p in procs]
        #
        # pool.close()
        # pool.join()
        #
        # log.info('completed processing parts')
        #
        # return

    ###################################################################
    # combine all parts to single file
    ###################################################################
    def combine_parts(self):

        out_path = self.output_path

        concat_option = 'concat:'
        for media in self.entry_data['media']:
            concat_option += media['part_file_path'] + '|'

        concat_option = concat_option[:-1]

        command = [
            'ffmpeg', '-i', concat_option, '-vn', '-ar', '44100', '-ac', '2', '-ab', '256k', '-f', 'mp3', '-y', out_path
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        process.wait()

        log.info('completed processing parts')

        return process.returncode

    ###################################################################
    # cleanup leftovers
    ###################################################################
    def cleanup(self):

        log.debug('cleaning: {}'.format(self.working_dir))
        if os.path.isdir(self.working_dir):
            shutil.rmtree(self.working_dir)

    def render(self, entry_uri, entry_id):

        self.prepare(uri=entry_uri, id=entry_id)

        self.download_media()
        self.process_parts()
        self.combine_parts()

        return self.output_path
