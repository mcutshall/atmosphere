# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-30 21:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_unique_allocationsource_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allocationsource',
            name='source_id',
        ),
    ]
