# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('genre', models.CharField(choices=[('Alternative', 'Alternative'), ('Anime', 'Anime'), ('Blues', 'Blues'), ('Childrens Music', 'Childrens Music'), ('Classical', 'Classical'), ('Comedy', 'Comedy'), ('Commercial', 'Commercial'), ('Country', 'Country'), ('Dance', 'Dance'), ('Electronic', 'Electronic'), ('Pop', 'Pop'), ('Indie', 'Indie'), ('Bluegrass', 'Bluegrass'), ('Gospel', 'Gospel'), ('Hip-Hop', 'Hip-Hop'), ('Rap', 'Rap'), ('Instrumental', 'Instrumental'), ('Jazz', 'Jazz'), ('Latin', 'Latin'), ('New Age', 'New Age'), ('R&B/Soul', 'R&B/Soul'), ('Reggae', 'Reggae'), ('Rock', 'Rock'), ('Singer', 'Singer'), ('Songwriter', 'Songwriter'), ('Vocal', 'Vocal'), ('World', 'World'), ('Metal', 'Metal'), ('Other', 'Other')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('rank', models.FloatField(default=0)),
                ('numerator', models.IntegerField(default=0)),
                ('denominator', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-rank'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('location', geoposition.fields.GeopositionField(blank=True, max_length=42)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('title', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('youtube_code', models.CharField(blank=True, max_length=20)),
                ('audio', models.FileField(blank=True, upload_to='audio/%Y/%m/%d/sound')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(blank=True, unique=True, max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('profile_image', models.ImageField(blank=True, upload_to='profile_image/%Y/%m/%d')),
                ('current_location', geoposition.fields.GeopositionField(blank=True, max_length=42)),
                ('is_musician', models.BooleanField(default=False)),
                ('search_range', models.IntegerField(default=30)),
                ('summary', models.TextField(blank=True)),
                ('company', models.CharField(blank=True, max_length=60)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SavedMusician',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('numbre', models.IntegerField()),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comrade',
            fields=[
                ('numbre', models.OneToOneField(serialize=False, primary_key=True, blank=True, to='profiles.SavedMusician')),
                ('date_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_stamp'],
            },
        ),
        migrations.AddField(
            model_name='savedmusician',
            name='saver_musician',
            field=models.ForeignKey(blank=True, null=True, to='profiles.Musician'),
        ),
        migrations.AddField(
            model_name='musician',
            name='friends',
            field=models.ManyToManyField(blank=True, to='profiles.SavedMusician'),
        ),
        migrations.AddField(
            model_name='musician',
            name='genres',
            field=models.ManyToManyField(blank=True, to='profiles.Genre'),
        ),
        migrations.AddField(
            model_name='musician',
            name='instruments',
            field=models.ManyToManyField(blank=True, to='profiles.Instrument'),
        ),
        migrations.AddField(
            model_name='musician',
            name='locations',
            field=models.ManyToManyField(blank=True, to='profiles.Location'),
        ),
        migrations.AddField(
            model_name='musician',
            name='media',
            field=models.ManyToManyField(blank=True, to='profiles.Media'),
        ),
        migrations.AddField(
            model_name='musician',
            name='comrades',
            field=models.ManyToManyField(blank=True, to='profiles.Comrade'),
        ),
    ]
