# Generated by Django 4.2.9 on 2024-04-09 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0005_tumortype_rename_scanaxis_scantype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanrecord',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 9, 21, 58, 12, 63429), verbose_name='Дата создания'),
        ),
    ]
