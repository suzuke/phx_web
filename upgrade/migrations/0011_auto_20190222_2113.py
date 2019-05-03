# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-22 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0010_svn_customer_t_zypismaster'),
    ]

    operations = [
        migrations.CreateModel(
            name='svn_zyp_lottery_gray_lock_t',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField(unique=True)),
                ('author', models.CharField(max_length=32)),
                ('date', models.CharField(max_length=32)),
                ('log', models.TextField(blank=True, null=True)),
                ('changelist', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='svn_customer_t',
            name='project',
            field=models.CharField(choices=[(b'other', b'\xe5\x85\xb6\xe4\xbb\x96[other]'), (b'caipiao', b'\xe5\xbd\xa9\xe7\xa5\xa8[caipiao]'), (b'zhuanyepan', b'\xe4\xb8\x93\xe4\xb8\x9a\xe7\x9b\x98[zyp]'), (b'sport', b'\xe4\xbd\x93\xe8\x82\xb2[sport]'), (b'houtai', b'\xe5\x90\x8e\xe5\x8f\xb0[houtai]'), (b'pay', b'\xe6\x94\xaf\xe4\xbb\x98[pay]'), (b'ggz', b'\xe5\xb9\xbf\xe5\x91\x8a\xe7\xab\x99[ggz]'), (b'image', b'\xe5\x9b\xbe\xe7\x89\x87[image]'), (b'vpn', b'vpn'), (b'httpdns', b'httpdns')], default='caipiao', max_length=10),
        ),
    ]