# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from profiles.choices_list import GENRES
from profiles.models import Genre

from django.db import models, migrations

def populate_genres(apps, schema_editor):
    genres = GENRES
    for genre in genres:
        Genre.objects.create(genre=genre[1])



class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20151122_0104'),
    ]

    operations = [
        migrations.RunPython(populate_genres),

    ]
