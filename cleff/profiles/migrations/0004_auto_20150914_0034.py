# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150913_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='name',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='comrade',
            name='date_stamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='description',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='musician',
            name='first_name',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='musician',
            name='last_name',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='musician',
            name='search_range',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='savedmusician',
            name='date_stamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
