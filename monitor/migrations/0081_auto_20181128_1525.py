# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0080_svn_master_t_svn_gray_lock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svn_master_t',
            name='svn_gray_lock',
            field=models.ManyToManyField(blank=True, null=True, to='upgrade.svn_gray_lock_t'),
        ),
    ]
