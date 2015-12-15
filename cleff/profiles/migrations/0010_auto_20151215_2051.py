# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20151215_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio/%Y/%m/%d/sound0.6422965842375156'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_image/%Y/%m/%d/0.30283123531496237'),
        ),
    ]
