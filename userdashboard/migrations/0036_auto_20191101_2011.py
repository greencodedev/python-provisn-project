# Generated by Django 2.2.6 on 2019-11-01 20:11

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0035_auto_20191101_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 20, 11, 30, 250145)),
        ),
        migrations.AlterField(
            model_name='tokenwatchlist',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
