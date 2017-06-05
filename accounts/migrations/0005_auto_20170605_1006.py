# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170605_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefered_cuisine',
            field=models.CharField(choices=[('GR', 'GREEK'), ('FR', 'FRENCH'), ('CHINESE', 'CHINESE'), ('INTERNATIONAL', 'INTERNATIONAL')], default='', max_length=15),
        ),
    ]
