# Generated by Django 2.2.18 on 2021-08-17 21:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20210815_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 19, 21, 35, 25, 733310, tzinfo=utc)),
        ),
    ]
