# Generated by Django 3.0 on 2020-02-08 02:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizbank', '0007_auto_20200131_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadtopic',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 8, 2, 3, 27, 795633, tzinfo=utc), verbose_name='last updated'),
        ),
    ]
