# Generated by Django 2.1.7 on 2019-02-26 12:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='customuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 28, 12, 48, 30, 858258, tzinfo=utc)),
        ),
    ]
