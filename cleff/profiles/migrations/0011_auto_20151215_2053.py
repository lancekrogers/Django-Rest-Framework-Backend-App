# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20151215_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio/%Y/%m/%d/sound0.04234403986959945'),
        ),
        migrations.AlterField(
            model_name='musician',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_image/%Y/%m/%d/0.6626455822080998'),
        ),
    ]
