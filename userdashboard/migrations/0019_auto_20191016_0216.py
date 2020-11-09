# Generated by Django 2.2.6 on 2019-10-16 02:16

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0018_auto_20191016_0037'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment_Errors',
            new_name='Payment_Error',
        ),
        migrations.AddField(
            model_name='payment_crypto',
            name='fulfilled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment_crypto',
            name='requested_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 2, 16, 2, 116397)),
        ),
    ]
