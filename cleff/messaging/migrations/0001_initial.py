# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20151126_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicianMusicianConversation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initializer', models.ForeignKey(to='profiles.Musician', related_name='initializer')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MusMusMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ManyToManyField(to='messaging.MusicianMusicianConversation')),
                ('receiver', models.ForeignKey(to='profiles.Musician', related_name='receiver')),
                ('sender', models.ForeignKey(to='profiles.Musician', related_name='sender')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='musicianmusicianconversation',
            name='messages',
            field=models.ManyToManyField(blank=True, to='messaging.MusMusMessage'),
        ),
        migrations.AddField(
            model_name='musicianmusicianconversation',
            name='musician_one',
            field=models.ForeignKey(to='profiles.Musician', related_name='musician_one'),
        ),
        migrations.AddField(
            model_name='musicianmusicianconversation',
            name='musician_two',
            field=models.ForeignKey(to='profiles.Musician', related_name='musician_two'),
        ),
    ]
