from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from hashlib import md5
from .utils import randomString
from jsonfield import JSONField
from uuid import uuid4

# from django.db.models.signals import post_save
# from django.dispatch import receiver


CURRENCIES = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
)


# Create your models here.
###
### Modified user model for the subscription
### userLevel = 0 : No subscription
### userLevel = 1 : Trial User
### userLevel = 2 : Subscribed user
### userLevel = 3 : Lifetime subscription
### userLevel = 4 : Lifetime subscription AND able to download user CSVs
class CustomUser(AbstractUser):
    userLevel = models.IntegerField(blank=False, default=1)
    sub_since = models.DateTimeField(default=timezone.now)
    sub_until = models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=15)))
    email = models.EmailField(_('email address'), unique=True)
    signup_token = models.CharField(max_length=128, blank=True, null=True)

    def get_remaining_subscription_time_in_days(self):
        time_left = None
        if self.sub_until > timezone.now():
            time_left = self.sub_until - timezone.now()
            time_left = time_left.days
        return time_left

    def get_subscription_time_text_class(self):
        if self.get_remaining_subscription_time_in_days() is not None:
            if self.get_remaining_subscription_time_in_days() < 3:
                return 'RED'
        return ''

    def update_referrer_token(self):
        ...

    def __str__(self):
        return self.username + ":" + self.email

    def get_referrer(self):
        from referral import utils
        return utils.getUserReferralTokenByToken(self.signup_token)


class Coin(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=128)
    coinpaprika_id = models.CharField(unique=True, max_length=256)
    coin_icon = models.ImageField(upload_to='coin_icons/', blank=True, null=True)
    description = models.TextField(blank=True)
    website_url = models.CharField(max_length=1000, blank=True)
    coinmarketcap_url = models.CharField(max_length=1000, blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name + ' [' + self.symbol + ']'


class Payment_Fiat(models.Model):
    session_id = models.TextField()
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    payment_amount = models.IntegerField()
    pricing = models.ForeignKey('Pricing_Fiat', on_delete=models.CASCADE, null=True)
    payment_fulfilled = models.BooleanField(default=False)
    requested_at = models.DateTimeField(default=timezone.now)
    fulfilled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'Paid: ' + str(self.payment_fulfilled) + ' | ' + str(self.user)


### Wrapper model for the cryptapi payment API which requires a unique order id so i had to add one
class Payment_Crypto(models.Model):
    coin = models.CharField(max_length=200)
    value = models.FloatField()
    browser_request = models.TextField()
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    auto_increment_id = models.AutoField(primary_key=True)
    pricing = models.ForeignKey('Pricing_Fiat', on_delete=models.CASCADE, blank=True, null=True)
    payment_done = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)
    payment_confirmation_log = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(default=timezone.now)
    fulfilled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.auto_increment_id) + ") " + self.user.__str__() + " Payment of " + str(self.value) + self.coin

    def add_log(self, log):
        try:
            if self.payment_confirmation_log is None:
                self.payment_confirmation_log = ''
            self.payment_confirmation_log = self.payment_confirmation_log + '\n' + log
            self.save()
        except Exception as exc:
            pass


class Pricing_Fiat(models.Model):
    cost_cent = models.IntegerField()
    subscription_time_in_days = models.IntegerField(default=30)
    stripe_recurring_plan = models.CharField(max_length=256, blank=True, null=True)
    recurring_only = models.BooleanField(default=False)
    amount_uses_usd = models.IntegerField(default=0)
    amount_uses_eth = models.IntegerField(default=0)
    amount_uses_btc = models.IntegerField(default=0)
    amount_uses_key = models.IntegerField(default=0)
    show_name = models.CharField(max_length=128, blank=True)
    show_on_page = models.BooleanField(default=False)
    only_available_using_key = models.BooleanField(default=False)
    key = models.CharField(max_length=64, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    saving = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.cost_cent) + ' (' + self.show_name + ')'

    def is_recurring(self):
        return True if self.stripe_recurring_plan is not None or self.stripe_recurring_plan != '' else False

    def get_crypto_value(self, currency='BTC'):
        try:
            value = Currency_Value.objects.filter(currency=currency).exclude(value_usd=None).latest('timestamp').value_usd
        except Currency_Value.DoesNotExist as dne:
            new = Currency_Value(
                currency=currency
            )
            new.save()
            value = Decimal(Currency_Value.objects.filter(currency=currency).exclude(value_usd=None).latest('timestamp').value_usd)
            pass
        try:
            value = Decimal(Decimal(self.cost_cent) / 100) / value
            round_place = 6 if currency == 'BTC' else 5
        except TypeError:
            return ''
        return round(value, round_place)

    def get_page_id(self):
        return randomString()

    def get_saving(self):
        pricings_credit_card_objects = Pricing_Fiat.objects.filter(show_on_page=True, only_available_using_key=False)
        this_saving = self.get_yearly_price_value()
        highest = None
        for pricing in pricings_credit_card_objects:
            value = pricing.get_yearly_price_value()
            if highest is None or highest < value:
                highest = value
        if this_saving != highest:
            return round(highest - this_saving)
        else:
            return

    def get_yearly_price_value(self):
        return 365 / self.subscription_time_in_days * (self.cost_cent * 10 ** -2)


class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    status = models.CharField(max_length=256)
    amount_due = models.IntegerField()
    amount_paid = models.IntegerField()
    amount_remaining = models.IntegerField()
    billing_type = models.CharField(max_length=256)
    billing_reason = models.CharField(max_length=256)
    currency = models.CharField(max_length=32)
    account_country = models.CharField(max_length=32, blank=True, null=True)
    invoice_id = models.CharField(max_length=256)
    invoice_url = models.URLField(blank=True, null=True)
    invoice_pdf = models.URLField(blank=True, null=True)
    payment_intent = models.CharField(max_length=256)
    payment_number = models.CharField(max_length=256)
    subscription_id = models.CharField(max_length=256, blank=True, null=True)
    payment_plan = models.CharField(max_length=256)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    data = models.ForeignKey('StripeWebhook', on_delete=models.CASCADE, related_name='webhook_log', blank=True,
                             null=True)

    def __str__(self):
        return str(self.user)


class ActiveSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sub_user')
    subscription = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='subscription')

    def __str__(self):
        return str(self.user) + str(self.subscription)


class StripeWebhook(models.Model):
    data = JSONField()

    def __str__(self):
        return str(self.data)


class UsedCoupon(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Pricing_Fiat', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.coupon) + ' ' + str(self.user)


'''
class Pricing_Crypto(models.Model):
    cost_ethereum = models.FloatField()
    only_available_using_key = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    discount_key = models.CharField(max_length=256, blank=True, null=True)
    subscription_time_in_days = models.IntegerField(default=30)
    show_on_page = models.BooleanField(default=False)
    amount_uses = models.IntegerField(default=0)
    show_name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return ('' if self.discount_key is None else ('[' +  self.discount_key + '] ')) + str(self.cost_ethereum) + ' ETH'

    def get_accepted_cost_value(self):
        return (self.cost_ethereum * (10 ** 18))
'''


class Payment_Error(models.Model):
    error_message = models.TextField()

    def __str__(self):
        return self.error_message[:32]


class Currency_Value(models.Model):
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    value_usd = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return self.currency + ' ' + str(self.value_usd) + ' @ ' + str(self.timestamp)


@receiver(post_save, sender=Currency_Value)
def currency_value_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    if instance.updated:
        if instance.timestamp is None or instance.value_usd is None:
            instance.delete()
        return
    from .utils import get_currency_value

    if instance.currency == 'BTC':
        data = get_currency_value('btc-bitcoin')
        instance.value_usd = data['quotes']['USD']['price']
    elif instance.currency == 'ETH':
        data = get_currency_value('eth-ethereum')
        instance.value_usd = data['quotes']['USD']['price']
    instance.updated = True
    instance.timestamp = timezone.now()
    instance.save()


class ChangeLog(models.Model):
    title = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class BugReport(models.Model):
    title = models.TextField(max_length=200)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    regard = models.TextField(max_length=256)
    status = models.CharField(max_length=128, default="OPEN")
    email = models.EmailField()
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '[' + self.status + ']' + '(' + str(self.created_date.strftime('%B %d %Y')) + ") " + str(
            self.user) + " | " + self.title


### Content Page Models ###

class BeamManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(text=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Beam(models.Model):
    pair = models.CharField(max_length=96)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    coinmarketcap_url = models.TextField(blank=True)
    entry = models.TextField(blank=True)
    targets = models.TextField(blank=True)
    stop_loss = models.TextField(blank=True)
    exchange = models.CharField(max_length=96, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    color_class = models.TextField(max_length=128, blank=True, null=True)

    @staticmethod
    def is_beam():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def get_block_id(self):
        # ToDo: Rework
        hash = md5(self.pair.encode('utf-8') + str(self.author).encode('utf-8') + self.targets.encode(
            'utf-8') + self.stop_loss.encode('utf-8') + str(self.created_date).encode('utf-8')).hexdigest()
        import re
        hash = re.sub('\W+', '', hash)

        return hash

    def get_icon_name_lowercase(self):
        return self.coin_shortname.lower()

    def get_model_name(self):
        return 'Beams'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '(' + str(self.created_date.strftime('%B %d %Y')) + ') ' + self.pair


class BeamsComment(models.Model):
    post = models.ForeignKey('userdashboard.Beam', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=1)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text


class BlockchainEventManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(text=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class BlockchainEvent(models.Model):
    title = models.TextField(max_length=256)
    date_of_event = models.DateTimeField(blank=True, null=True, default=timezone.now)
    text = RichTextField()
    venue = models.TextField(max_length=256, blank=True)
    location = models.TextField(max_length=256, blank=True)
    event_url = models.URLField(blank=True, max_length=1024)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    set_color = models.BooleanField(default=False)
    color_class = models.TextField(max_length=128, default='event_color_green')

    @staticmethod
    def is_event():
        return True

    def get_model_name(self):
        return 'Events'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __lt__(self, other):
        return self.date_of_event > other.date_of_event

    @property
    def get_html_url(self):
        if self.event_url:
            return f'<a href="{self.event_url}" target="_blank"> <div class="event {self.color_class}">{self.title}</div> </a>'
        else:
            url = reverse('DetailsEvents', args=(self.id,))
            return f'<a href="{url}"><div class="event {self.color_class}">{self.title}</div></a>'

    def __str__(self):
        return '(' + str(self.date_of_event.strftime('%B %d %Y')) + ') ' + self.title

    class Meta:
        unique_together = ['title', 'date_of_event', 'text']


### Handles setting color after saving
@receiver(post_save, sender=BlockchainEvent)
def event_save_handler(sender, **kwargs):
    if kwargs['instance'].set_color is True:
        return
    if 'Conference' in kwargs['instance'].title or 'conference' in kwargs['instance'].title:
        kwargs['instance'].color_class = 'event_color_blue'
        kwargs['instance'].set_color = True
        kwargs['instance'].save()


class BlockchainEventsComment(models.Model):
    post = models.ForeignKey('userdashboard.BlockchainEvent', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text


class BlockchainNew(models.Model):
    title = models.TextField(max_length=512)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    # news_image = models.ImageField(upload_to='news_images/' + unidecode.unidecode(str(timezone.now())), blank=True, null=True)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)

    @staticmethod
    def is_news():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def get_value_shadow_class(self):
        return 'z-depth-%d' % self.value

    def get_model_name(self):
        return 'News'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '(' + str(self.created_date.strftime('%B %d %Y')) + ') ' + self.title


class BlockchainNewsComment(models.Model):
    post = models.ForeignKey('userdashboard.BlockchainNew', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text


class ArtificialIntelligence(models.Model):
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    has_been_cleaned_up = models.BooleanField(default=False)

    @staticmethod
    def is_ai():
        return True

    def get_text_field(self):
        pos = self.get_percentage_value_position()
        return self.text[:pos] + '<div class="d-none">' + self.text[pos:] + '</div>'

    def get_model_name(self):
        return 'Artificial Intelligence'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_percentage_value(self):
        percentageValuePosition = self.get_percentage_value_position() + 15
        percentageValue = self.text[percentageValuePosition:percentageValuePosition + 5].replace('%', '').replace('<',
                                                                                                                  '').replace(
            '>', '')
        if 'ng' in percentageValue:
            percentageValue = self.text[percentageValuePosition + 4:percentageValuePosition + 9].replace('%',
                                                                                                         '').replace(
                '<', '').replace('>', '')
        return percentageValue

    def get_percentage_value_number(self):
        try:
            percentageValueNumber = float(self.get_percentage_value())
            return percentageValueNumber
        except Exception:
            pass

    def get_percentage_value_in_deg(self):
        percentageValueInDeg = 180 / 100 * float(self.get_percentage_value_number())
        return percentageValueInDeg

    def get_gauge_class(self):
        GaugeClass = ''
        if self.get_percentage_value_number() >= 75:
            GaugeClass = 'indicator-green'
        elif self.get_percentage_value_number() >= 50:
            GaugeClass = 'indicator-blue'
        elif self.get_percentage_value_number() >= 25:
            GaugeClass = 'indicator-yellow'
        else:
            GaugeClass = 'indicator-red'
        return GaugeClass

    def get_percentage_value_position(self):
        pos = self.text.find('Indicator')
        return pos

    def __str__(self):
        return str(self.created_date.strftime('%B %d %Y')) + self.get_percentage_value() + '%'


@receiver(post_save, sender=ArtificialIntelligence)
def cleanup_ci_message(sender, **kwargs):
    instance = kwargs['instance']
    if instance.has_been_cleaned_up:
        return
    offset = instance.text.find('. Will') + 2
    if offset == 1:
        offset = instance.text.find(', will') + 2
    instance.text = instance.text[offset:]
    instance.text = instance.text.replace('will', 'Will')

    offset_question_end = instance.text.find('?') + 1
    offset_indicator_start = instance.text.find('<strong>')
    text_remove_part = instance.text[offset_question_end: offset_indicator_start]
    instance.text = instance.text.replace(text_remove_part, '<br/>')

    if instance.text.startswith('p>'):
        instance.text = instance.text.replace('p>', '', 1)
    instance.has_been_cleaned_up = True
    instance.save()
    print(offset)


class ArtificialIntelligenceComment(models.Model):
    post = models.ForeignKey('userdashboard.ArtificialIntelligence', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text


class TechnicalAnalysi(models.Model):
    title = models.TextField(max_length=512)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = RichTextField()
    notes = RichTextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)

    @staticmethod
    def is_ta():
        return True

    def get_value_shadow_class(self):
        return 'z-depth-%d' % self.value

    def get_model_name(self):
        return 'Technical Analysis'

    def __lt__(self, other):
        return self.published_date > other.published_date

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '(' + str(self.created_date.strftime('%B %d %Y')) + ') ' + self.title


class TechnicalAnalysisComment(models.Model):
    post = models.ForeignKey('userdashboard.TechnicalAnalysi', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text


class TokenWatchlist(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, blank=True, null=True)
    coin_icon = models.ImageField(upload_to='token_spotlight_icons/' + str(uuid4()) + '/', blank=True, null=True)
    About = RichTextField(blank=True)
    Product = RichTextField(blank=True)
    Team = RichTextField(blank=True)
    Value = RichTextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    up_votes = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)

    @staticmethod
    def is_tw():
        return True

    def get_icon_name_lowercase(self):
        return self.coin_shortname.lower()

    def get_value_shadow_class(self):
        return 'z-depth-%d' % self.value

    def get_model_name(self):
        return 'Token Watchlist'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '(' + str(self.created_date.strftime('%B %d %Y')) + ') ' + str(self.coin)


class TokenWatchlistComment(models.Model):
    post = models.ForeignKey('userdashboard.TokenWatchlist', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
        return self.comments.filter(approved_comment=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '(' + str(self.author) + ') ' + self.text
