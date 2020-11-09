# Generated by Django 2.2.4 on 2019-09-05 16:09

import ckeditor.fields
import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userLevel', models.IntegerField(default=1)),
                ('sub_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('sub_until', models.DateTimeField(default=datetime.datetime(2019, 9, 20, 16, 9, 5, 44513))),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('signup_token', models.CharField(blank=True, max_length=128, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ArtificialIntelligence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('value', models.IntegerField(default=0)),
                ('up_votes', models.IntegerField(default=0)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Beam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.CharField(max_length=96)),
                ('coinmarketcap_url', models.TextField(blank=True)),
                ('entry', models.TextField(blank=True)),
                ('targets', models.TextField(blank=True)),
                ('stop_loss', models.TextField(blank=True)),
                ('exchange', models.CharField(blank=True, max_length=96)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('value', models.IntegerField(default=0)),
                ('up_votes', models.IntegerField(default=0)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlockchainEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=256)),
                ('date_of_event', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('text', ckeditor.fields.RichTextField()),
                ('venue', models.TextField(blank=True, max_length=256)),
                ('location', models.TextField(blank=True, max_length=256)),
                ('event_url', models.URLField(blank=True, max_length=1024)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'unique_together': {('title', 'date_of_event', 'text')},
            },
        ),
        migrations.CreateModel(
            name='BlockchainNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=512)),
                ('text', ckeditor.fields.RichTextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('value', models.IntegerField(default=0)),
                ('up_votes', models.IntegerField(default=0)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('symbol', models.CharField(max_length=10)),
                ('slug', models.CharField(max_length=128)),
                ('cmc_id', models.BigIntegerField()),
                ('coin_icon', models.ImageField(blank=True, null=True, upload_to='coin_icons/')),
                ('description', models.TextField(blank=True)),
                ('website_url', models.CharField(blank=True, max_length=1000)),
                ('coinmarketcap_url', models.CharField(blank=True, max_length=1000)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_ethereum', models.FloatField()),
                ('only_available_using_key', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=False)),
                ('discount_key', models.CharField(blank=True, max_length=256, null=True)),
                ('subscription_time_in_days', models.IntegerField(default=30)),
                ('show_on_page', models.BooleanField(default=False)),
                ('amount_uses', models.IntegerField(default=0)),
                ('show_name', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalAnalysi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=512)),
                ('text', ckeditor.fields.RichTextField()),
                ('notes', ckeditor.fields.RichTextField(blank=True)),
                ('diagram_embed', models.TextField(blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('value', models.IntegerField(default=0)),
                ('up_votes', models.IntegerField(default=0)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='TokenWatchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=256)),
                ('text', ckeditor.fields.RichTextField()),
                ('Current_Value', models.FloatField(blank=True, null=True)),
                ('ATH', models.FloatField(blank=True, null=True)),
                ('ATL', models.FloatField(blank=True, null=True)),
                ('Market_Cap', models.FloatField(blank=True, null=True)),
                ('Volume_24h', models.FloatField(blank=True, null=True)),
                ('Supply', models.TextField(blank=True)),
                ('Change_24h', models.FloatField(blank=True, null=True)),
                ('Change_7d', models.FloatField(blank=True, null=True)),
                ('News', ckeditor.fields.RichTextField(blank=True)),
                ('Social', ckeditor.fields.RichTextField(blank=True)),
                ('Markets', ckeditor.fields.RichTextField(blank=True)),
                ('Specifications', ckeditor.fields.RichTextField(blank=True)),
                ('Team', ckeditor.fields.RichTextField(blank=True)),
                ('Tokenomics', ckeditor.fields.RichTextField(blank=True)),
                ('Value', ckeditor.fields.RichTextField(blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('up_votes', models.IntegerField(default=0)),
                ('has_been_sent_to_telegram', models.BooleanField(default=False)),
                ('has_been_sent_to_telegram_for_unsubscribed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userdashboard.Coin')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='TokenWatchlistComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.TokenWatchlist')),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalAnalysisComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.TechnicalAnalysi')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('coin', models.CharField(max_length=200)),
                ('value', models.FloatField()),
                ('browser_request', models.TextField()),
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_done', models.BooleanField(default=False)),
                ('payment_received', models.BooleanField(default=False)),
                ('pricing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userdashboard.Pricing')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('text', ckeditor.fields.RichTextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('regard', models.TextField(max_length=256)),
                ('status', models.CharField(default='OPEN', max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlockchainNewsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.BlockchainNew')),
            ],
        ),
        migrations.CreateModel(
            name='BlockchainEventsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.BlockchainEvent')),
            ],
        ),
        migrations.CreateModel(
            name='BeamsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.Beam')),
            ],
        ),
        migrations.AddField(
            model_name='beam',
            name='coin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userdashboard.Coin'),
        ),
        migrations.AddField(
            model_name='beam',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='ArtificialIntelligenceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=256)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('value', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userdashboard.ArtificialIntelligence')),
            ],
        ),
    ]