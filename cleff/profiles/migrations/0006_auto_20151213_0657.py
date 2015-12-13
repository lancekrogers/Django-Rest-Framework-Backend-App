# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20151212_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='media',
            field=models.ManyToManyField(to='profiles.Media', blank=True),
        ),
    ]
