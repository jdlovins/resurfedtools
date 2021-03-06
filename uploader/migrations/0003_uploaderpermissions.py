# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_auto_20171118_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploaderPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('uploader_access', 'Can access the uploader'), ('uploader_admin', 'Has access to the advanced uploader options')),
                'managed': False,
            },
        ),
    ]
