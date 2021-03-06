# Generated by Django 2.2.4 on 2019-09-20 18:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('byName', models.CharField(max_length=200)),
                ('email_ticket', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(default='OPEN', max_length=128)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
