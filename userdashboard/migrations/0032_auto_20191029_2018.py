# Generated by Django 2.2.6 on 2019-10-29 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0031_auto_20191028_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coin',
            old_name='cmc_id',
            new_name='coinpaprika_id',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 13, 20, 18, 8, 255495)),
        ),
    ]
