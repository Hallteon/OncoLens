# Generated by Django 4.2.9 on 2024-04-12 16:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_patient_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 21, 45, 6, 513150), verbose_name='Дата создания'),
        ),
    ]