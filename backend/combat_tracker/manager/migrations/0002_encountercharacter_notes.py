# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encountercharacter',
            name='notes',
            field=models.CharField(default='', max_length=128),
        ),
    ]
