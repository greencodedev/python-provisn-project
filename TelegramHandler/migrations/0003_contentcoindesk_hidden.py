# Generated by Django 2.2.6 on 2019-11-09 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TelegramHandler', '0002_auto_20190928_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentcoindesk',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
