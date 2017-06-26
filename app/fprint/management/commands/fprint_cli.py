#-*- coding: utf-8 -*-

import time
import sys
import json
import datetime
from django.conf import settings
import random
import string
import requests
from django.utils import timezone
import djclick as click
from django.conf import settings

from ...models import Entry
from ...utils import build_index
from ...backend import FprintBackend


RUN_ASYNC = getattr(settings, 'MATCHING_RUN_ASYNC', False)
ALWAYS_UPDATE = getattr(settings, 'MATCHING_ALWAYS_UPDATE', False)


@click.group()
def cli():
    pass

@cli.command()
def ingest():

    b = FprintBackend()

    b.build_index()


    # with click.progressbar(qs, label='build index', length=qs.count()) as bar:
    #
    #     for item in bar:
    #         build_inverted_index()
    #
    #         time.sleep(0.2)

@cli.command()
def reset():

    if click.confirm('Do you really want to reset the database?'):
        click.echo(Entry.objects.all().delete())




@cli.command()
def test_codes():
    qs = Entry.objects.filter().order_by('-created')

    num_match = 0
    num_mismatch = 0

    for entry in qs:

        data = {
            'code': entry.code
        }

        url = 'http://127.0.0.1:7777/api/v1/fprint/identify/'
        r = requests.post(url, json=data)

        # click.echo('-')
        # click.secho('{} - {}'.format(r.status_code, len(entry.code)), fg='cyan')

        results = r.json()

        uuid = results[0]['uuid']
        score = results[0]['score']

        # click.secho('result:   {} - {}'.format(uuid, score), fg='cyan')
        # click.secho('original: {}'.format(entry.uuid), fg='cyan')


        score_list = ['{}'.format(r['score']) for r in results]

        # print(score_list)

        match = (str(uuid) == str(entry.uuid))

        if match:
            #click.secho('match!', fg='green')
            num_match += 1
        else:

            click.secho('result:   {} - {}'.format(uuid, score), fg='cyan')
            click.secho('original: {}'.format(entry.uuid), fg='cyan')
            click.secho('wrong match!', fg='red')
            print(score_list)
            num_mismatch += 1


    click.echo('*' * 72)
    click.secho('Total matches:    {}'.format(num_match), fg='green')
    click.secho('Total mismatches: {}'.format(num_mismatch), fg='red')
    click.secho('Total entries:    {}'.format(qs.count()), fg='white')




