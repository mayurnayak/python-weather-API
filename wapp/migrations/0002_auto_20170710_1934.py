# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='wid_city',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='zip_code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]