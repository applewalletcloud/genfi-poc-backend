# Generated by Django 3.0 on 2020-05-16 00:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizbank', '0012_auto_20200513_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main_post', models.BooleanField(default=False)),
                ('post_id', models.IntegerField()),
                ('main_post_id', models.IntegerField()),
                ('parent_id', models.IntegerField()),
                ('creator', models.CharField(max_length=255)),
                ('post_title', models.TextField()),
                ('post_text', models.TextField()),
                ('created_on', models.DateTimeField(default=datetime.datetime(2020, 5, 16, 0, 44, 40, 75169, tzinfo=utc), verbose_name='date published')),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime(2020, 5, 16, 0, 44, 40, 75187, tzinfo=utc), verbose_name='last updated')),
                ('indentation_level', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='forumuserprofilepic',
            name='profile_pic',
            field=models.ImageField(upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='threadtopic',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 16, 0, 44, 40, 73695, tzinfo=utc), verbose_name='last updated'),
        ),
    ]
