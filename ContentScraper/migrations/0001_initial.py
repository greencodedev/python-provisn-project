# Generated by Django 2.2.4 on 2019-09-12 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content_safe_signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_Moiseiev_Yurii',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_KhaledAbdulaziz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_HamadaMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_Faibik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_ArShevelev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
        migrations.CreateModel(
            name='Content_alanmasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('db_diagram_embed', models.TextField(blank=True)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('title', 'text', 'diagram_embed')},
            },
        ),
    ]
