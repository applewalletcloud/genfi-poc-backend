# Generated by Django 3.0 on 2020-02-08 02:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizbank', '0008_auto_20200208_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadtopic',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 8, 2, 23, 42, 765257, tzinfo=utc), verbose_name='last updated'),
        ),
    ]
