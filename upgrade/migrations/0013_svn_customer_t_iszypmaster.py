# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-23 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0012_svn_customer_t_isrsynczypcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='svn_customer_t',
            name='iszypmaster',
            field=models.IntegerField(choices=[(1, b'\xe5\x90\xaf\xe7\x94\xa8'), (0, b'\xe7\xa6\x81\xe7\x94\xa8')], default=0),
        ),
    ]