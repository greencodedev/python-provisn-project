# Generated by Django 2.2.6 on 2019-11-01 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0034_auto_20191029_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='ATH',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='ATL',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Change_24h',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Change_7d',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Current_Value',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Market_Cap',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='News',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Social',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Supply',
        ),
        migrations.RemoveField(
            model_name='tokenwatchlist',
            name='Volume_24h',
        ),
        migrations.AddField(
            model_name='tokenwatchlist',
            name='coin_icon',
            field=models.ImageField(blank=True, null=True, upload_to='token_spotlight_icons/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 20, 9, 38, 295482)),
        ),
    ]