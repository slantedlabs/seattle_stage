# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0005_auto_20170213_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='blurb',
            field=models.TextField(null=True),
        ),
    ]
