# Generated by Django 2.2.5 on 2019-10-10 01:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0008_auto_20191009_0444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricing_fiat',
            old_name='cost_usd_cent',
            new_name='cost_cent',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 25, 1, 31, 18, 330225)),
        ),
    ]