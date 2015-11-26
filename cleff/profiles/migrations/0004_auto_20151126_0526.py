# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_load_instruments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='denominator',
            field=models.IntegerField(default=1),
        ),
    ]
