# Generated by Django 4.2.9 on 2024-04-14 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_patient_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 23, 30, 35, 430167), verbose_name='Дата создания'),
        ),
    ]