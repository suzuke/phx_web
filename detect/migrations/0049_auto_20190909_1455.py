# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-09 14:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0048_auto_20190805_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegram_chat_group_t',
            name='group_id',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]