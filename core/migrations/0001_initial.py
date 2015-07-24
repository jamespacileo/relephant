# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('command', models.CharField(null=True, blank=True, choices=[('up', 'up'), ('down', 'down'), ('left', 'left'), ('right', 'right'), ('a', 'a'), ('b', 'b')], db_index=True, max_length=100)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
    ]
