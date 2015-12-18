# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20151218_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='search_range',
            field=profiles.models.MaxOrMinIntegerField(default=30),
        ),
    ]
