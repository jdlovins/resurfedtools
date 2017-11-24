# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 16:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0003_uploaderpermissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploaderpermissions',
            options={'managed': False, 'permissions': (('uploader_access', 'Can access the uploader'), ('uploader_admin', 'Has uploader admin access'))},
        ),
    ]