# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20151214_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='audio',
            field=models.FileField(upload_to='audio/%Y/%m/%d/sound0.4130767634117589', blank=True),
        ),
        migrations.AlterField(
            model_name='musician',
            name='profile_image',
            field=models.ImageField(upload_to='profile_image/%Y/%m/%d/0.6186877500419881', blank=True),
        ),
    ]
