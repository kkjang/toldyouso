# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField()),
                ('room_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=255)),
                ('ready', models.BooleanField()),
                ('challenger_bet', models.TextField()),
                ('challenged_bet', models.TextField()),
            ],
        ),
    ]
