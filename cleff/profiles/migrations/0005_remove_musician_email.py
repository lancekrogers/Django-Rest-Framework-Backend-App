# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20150914_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musician',
            name='email',
        ),
    ]
