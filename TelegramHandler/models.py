from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib.parse import unquote


class TelegramAccountWrapper(models.Model):
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    telegram_name = models.CharField(max_length=256, blank=True)
    token = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return str(self.account) + ' - ' + self.telegram_name


class TelegramActiveUsersBroadcast(models.Model):
    Wrapper = models.ForeignKey(TelegramAccountWrapper, on_delete=models.CASCADE)
    User_Id = models.BigIntegerField()

    def __str__(self):
        return str(self.Wrapper.account) + ' - ' + self.Wrapper.telegram_name


class TelegramActiveUsersChat(models.Model):
    Wrapper = models.ForeignKey(TelegramAccountWrapper, on_delete=models.CASCADE)
    User_Id = models.BigIntegerField()

    def __str__(self):
        return str(self.Wrapper.account) + ' - ' + self.Wrapper.telegram_name



class ContentCoinDesk(models.Model):
    title = models.TextField(max_length=256, blank=True)
    text = models.TextField(unique=True)
    published_date = models.DateTimeField()
    is_coin_desk_content = models.BooleanField(default=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    image_url = models.TextField(max_length=512, null=True, blank=True)
    information_updated = models.BooleanField(default=False)
    news_url = models.TextField(max_length=512, null=True, blank=True)
    hidden = models.BooleanField(default=False)

    @staticmethod
    def is_news():
        return True

    def get_url(self):
        return unquote(self.news_url) if self.news_url else ''

    def __str__(self):
        return self.text

    def __lt__(self, other):
        return self.published_date > other.published_date

    def get_title(self):
        return self.title.replace(' - CoinDesk', '')

    class Meta:
        unique_together = ['text', 'published_date']


@receiver(post_save, sender=ContentCoinDesk)
def update_news_information(sender, **kwargs):
    from userdashboard.utils import update_news_article
    update_news_article(kwargs['instance'])


