# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehouse',
            options={'verbose_name': 'Magazzino', 'verbose_name_plural': 'Magazzino'},
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='name',
        ),
    ]