# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatprofile',
            name='num_of_room_available',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=10),
        ),
    ]