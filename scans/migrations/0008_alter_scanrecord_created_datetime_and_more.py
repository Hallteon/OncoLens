# Generated by Django 4.2.9 on 2024-04-12 16:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0007_tumortype_tumor_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanrecord',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 21, 47, 2, 416496), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='tumortype',
            name='tumor_type',
            field=models.CharField(max_length=255, unique=True, verbose_name='Тип'),
        ),
    ]