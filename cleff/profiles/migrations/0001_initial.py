# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('genre', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('family', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=50, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('location', geoposition.fields.GeopositionField(max_length=42, blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user_pk', models.IntegerField(default=-1)),
                ('title', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('embedded_code', models.CharField(max_length=20, blank=True)),
                ('upload', models.FileField(blank=True, upload_to='video/%Y/%m/%d/title')),
                ('genre', models.ManyToManyField(to='profiles.Genre', blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('first_name', models.CharField(max_length=15, blank=True)),
                ('last_name', models.CharField(max_length=15, blank=True)),
                ('profile_image', models.ImageField(blank=True, upload_to='profile_image/%Y/%m/%d')),
                ('current_location', geoposition.fields.GeopositionField(max_length=42, blank=True)),
                ('is_musician', models.BooleanField(default=False)),
                ('search_range', models.IntegerField(default=50)),
                ('summary', models.TextField(blank=True)),
                ('company', models.CharField(max_length=60, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SavedMusician',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('numbre', models.IntegerField()),
                ('date_stamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comrade',
            fields=[
                ('numbre', models.OneToOneField(primary_key=True, to='profiles.SavedMusician', blank=True, serialize=False)),
                ('date_stamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_stamp'],
            },
        ),
        migrations.AddField(
            model_name='savedmusician',
            name='saver_musician',
            field=models.ForeignKey(blank=True, to='profiles.Musician', null=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='friends',
            field=models.ManyToManyField(to='profiles.SavedMusician', blank=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='genres',
            field=models.ManyToManyField(to='profiles.Genre', blank=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='instruments',
            field=models.ManyToManyField(to='profiles.Instrument', blank=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='locations',
            field=models.ManyToManyField(to='profiles.Location', blank=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='media',
            field=models.ManyToManyField(to='profiles.Media', blank=True),
        ),
        migrations.AddField(
            model_name='musician',
            name='comrades',
            field=models.ManyToManyField(to='profiles.Comrade', blank=True),
        ),
    ]
