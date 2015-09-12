# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='embedded_code',
            new_name='youtube_code',
        ),
        migrations.RemoveField(
            model_name='media',
            name='upload',
        ),
        migrations.AddField(
            model_name='media',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio/%Y/%m/%d/sound'),
        ),
        migrations.AddField(
            model_name='media',
            name='video',
            field=models.FileField(blank=True, upload_to='video/%Y/%m/%d/video'),
        ),
    ]
