# Generated by Django 2.1.7 on 2019-03-05 09:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20190301_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 7, 9, 53, 55, 498913, tzinfo=utc)),
        ),
    ]