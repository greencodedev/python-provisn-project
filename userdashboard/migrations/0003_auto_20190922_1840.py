# Generated by Django 2.2.4 on 2019-09-22 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0002_auto_20190912_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchainevent',
            name='color_class',
            field=models.TextField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 18, 40, 8, 942189)),
        ),
    ]
