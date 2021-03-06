# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Initialized'), (1, 'Pending'), (2, 'Done'), (99, 'Error')], db_index=True, default=1, verbose_name='Status')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='The UUID is is set from "outside"/client when ingesting a fingerprint')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('code', models.TextField(null=True)),
            ],
        ),
    ]
