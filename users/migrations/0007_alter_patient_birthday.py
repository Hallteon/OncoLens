# Generated by Django 4.2.6 on 2024-03-23 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_patient_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 23, 23, 21, 12, 318016), verbose_name='Дата создания'),
        ),
    ]