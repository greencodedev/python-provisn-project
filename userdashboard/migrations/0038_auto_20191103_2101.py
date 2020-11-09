# Generated by Django 2.2.6 on 2019-11-03 21:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0037_auto_20191101_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 21, 1, 58, 487177)),
        ),
        migrations.AlterField(
            model_name='tokenwatchlist',
            name='coin_icon',
            field=models.ImageField(blank=True, null=True, upload_to='token_spotlight_icons/27e2be25-6086-4bcb-8be3-fdcc58d5905f/'),
        ),
    ]
