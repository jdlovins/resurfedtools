# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0005_auto_20171123_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionInfo',
            fields=[
                ('server', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='uploader.Server')),
                ('connection', models.CharField(choices=[('FTP', 'FTP'), ('FTPS', 'FTPS'), ('SFTP', 'SFTP')], max_length=10)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('host_address', models.CharField(max_length=32)),
                ('port', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='server',
            name='connection',
        ),
        migrations.RemoveField(
            model_name='server',
            name='host_address',
        ),
        migrations.RemoveField(
            model_name='server',
            name='order',
        ),
        migrations.RemoveField(
            model_name='server',
            name='password',
        ),
        migrations.RemoveField(
            model_name='server',
            name='port',
        ),
        migrations.RemoveField(
            model_name='server',
            name='username',
        ),
    ]
