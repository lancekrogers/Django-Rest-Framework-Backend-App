# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150912_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='family',
        ),
        migrations.RemoveField(
            model_name='location',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='media',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='media',
            name='video',
        ),
        migrations.AddField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 4, 46, 50, 145838, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=20, choices=[('Alternative', 'Alternative'), ('Anime', 'Anime'), ('Blues', 'Blues'), ('Childrens Music', 'Childrens Music'), ('Classical', 'Classical'), ('Comedy', 'Comedy'), ('Commercial', 'Commercial'), ('Country', 'Country'), ('Dance', 'Dance'), ('Electronic', 'Electronic'), ('Pop', 'Pop'), ('Indie', 'Indie'), ('Bluegrass', 'Bluegrass'), ('Gospel', 'Gospel'), ('Hip-Hop', 'Hip-Hop'), ('Rap', 'Rap'), ('Instrumental', 'Instrumental'), ('Jazz', 'Jazz'), ('Latin', 'Latin'), ('New Age', 'New Age'), ('R&B/Soul', 'R&B/Soul'), ('Reggae', 'Reggae'), ('Rock', 'Rock'), ('Singer', 'Singer'), ('Songwriter', 'Songwriter'), ('Vocal', 'Vocal'), ('World', 'World'), ('Metal', 'Metal'), ('Other', 'Other')]),
        ),
    ]
