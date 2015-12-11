# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20151126_0526'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='TheConversation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initializer', models.ForeignKey(to='profiles.Musician', related_name='initializer')),
                ('messages', models.ManyToManyField(to='messaging.Message', blank=True)),
                ('musician_one', models.ForeignKey(to='profiles.Musician', related_name='musician_one')),
                ('musician_two', models.ForeignKey(to='profiles.Musician', related_name='musician_two')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.RemoveField(
            model_name='musicianmusicianconversation',
            name='initializer',
        ),
        migrations.RemoveField(
            model_name='musicianmusicianconversation',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='musicianmusicianconversation',
            name='musician_one',
        ),
        migrations.RemoveField(
            model_name='musicianmusicianconversation',
            name='musician_two',
        ),
        migrations.RemoveField(
            model_name='musmusmessage',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='musmusmessage',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='musmusmessage',
            name='sender',
        ),
        migrations.DeleteModel(
            name='MusicianMusicianConversation',
        ),
        migrations.DeleteModel(
            name='MusMusMessage',
        ),
        migrations.AddField(
            model_name='message',
            name='conversation',
            field=models.ManyToManyField(to='messaging.TheConversation'),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(to='profiles.Musician', related_name='receiver'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(to='profiles.Musician', related_name='sender'),
        ),
    ]
