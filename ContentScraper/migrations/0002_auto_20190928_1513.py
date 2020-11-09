# Generated by Django 2.2.4 on 2019-09-28 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentScraper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content_CryptoNTez',
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
            name='Fear_and_Greed_Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('value_classification', models.CharField(max_length=128)),
                ('update_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Content_ArShevelev',
        ),
        migrations.DeleteModel(
            name='Content_HamadaMark',
        ),
        migrations.DeleteModel(
            name='Content_Moiseiev_Yurii',
        ),
        migrations.DeleteModel(
            name='Content_safe_signal',
        ),
    ]