# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
