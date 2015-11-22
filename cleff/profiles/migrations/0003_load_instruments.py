# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from profiles.choices_list import INSTRUMENT_CLASSES
from profiles.models import Instrument

from django.db import models, migrations

def populate_instruments(apps, schema_editor):
    instruments = INSTRUMENT_CLASSES
    for instrument in instruments:
        Instrument.objects.create(name=instrument[1])



class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_load_genres'),
    ]

    operations = [
        migrations.RunPython(populate_instruments),

    ]
