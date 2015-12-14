# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20151213_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio/%Y/%m/%d/sound0.2355710228431993'),
        ),
    ]
