# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-22 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0026_svn_zyp_front2_gray_lock_t'),
        ('monitor', '0099_auto_20191028_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='svn_master_t',
            name='svnzypfront2_gray_lock',
            field=models.ManyToManyField(blank=True, to='upgrade.svn_zyp_front2_gray_lock_t'),
        ),
    ]
