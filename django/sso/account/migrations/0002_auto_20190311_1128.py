# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-11 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
