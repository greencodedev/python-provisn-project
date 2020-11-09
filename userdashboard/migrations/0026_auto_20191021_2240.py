# Generated by Django 2.2.6 on 2019-10-21 22:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0025_auto_20191021_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing_fiat',
            name='stripe_recurring_plan',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 22, 40, 11, 712261)),
        ),
    ]
