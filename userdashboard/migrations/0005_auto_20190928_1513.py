# Generated by Django 2.2.4 on 2019-09-28 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0004_auto_20190922_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='artificialintelligence',
            name='has_been_cleaned_up',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='beam',
            name='color_class',
            field=models.TextField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='blockchainevent',
            name='color_class',
            field=models.TextField(default='indicator-yellow', max_length=128),
        ),
        migrations.AlterField(
            model_name='coin',
            name='cmc_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 13, 15, 13, 36, 757865)),
        ),
    ]
