# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0008_alter_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='dnspod_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('email', models.CharField(max_length=128)),
                ('key', models.CharField(max_length=128)),
            ],
        ),
    ]
