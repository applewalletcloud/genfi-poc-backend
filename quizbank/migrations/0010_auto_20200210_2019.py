# Generated by Django 3.0 on 2020-02-10 20:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizbank', '0009_auto_20200208_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadtopic',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 10, 20, 19, 32, 115951, tzinfo=utc), verbose_name='last updated'),
        ),
    ]
