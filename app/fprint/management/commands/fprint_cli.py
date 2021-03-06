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

from ...models import Entry, CODES_PER_INDEX
from ...backend import FprintBackend


PUBLIC_APP_URL = getattr(settings, 'PUBLIC_APP_URL')


@click.group()
def cli():
    pass

@cli.command()
@click.option('--force', default=False, is_flag=True, help='Force to rebuild index?')
def update_index(force):
    """
    update fprint index.
    """

    b = FprintBackend()
    b.build_index(force_rebuild=force)


@cli.command()
def reset():
    """
    reset fprint db.
    """

    if click.confirm('Do you really want to reset the database?'):
        click.echo(Entry.objects.all().delete())



@cli.command()
@click.option('--id', type=int)
def test_codes(id):

    qs = Entry.objects.filter().order_by('-created')

    if id:
        qs = qs.filter(pk__in=[id])

    num_match = 0
    num_mismatch = 0

    for entry in qs:

        data = {
            'code': entry.code
        }

        url = '{}/api/v1/fprint/identify/'.format(PUBLIC_APP_URL)
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




