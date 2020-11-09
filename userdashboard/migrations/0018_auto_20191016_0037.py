# Generated by Django 2.2.6 on 2019-10-16 00:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0017_auto_20191016_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Errors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_message', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Pricing',
            new_name='Pricing_Crypto',
        ),
        migrations.AddField(
            model_name='payment_crypto',
            name='payment_confirmation_log',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pricing_fiat',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pricing_fiat',
            name='only_available_using_key',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sub_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 0, 37, 47, 142103)),
        ),
    ]
