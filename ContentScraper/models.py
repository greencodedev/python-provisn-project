from django.db import models


class Content_Faibik(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    published_date = models.DateTimeField(auto_now=True, editable=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @staticmethod
    def is_ta_Faibik():
        return True

    @staticmethod
    def is_ta_scraped():
        return True

    @staticmethod
    def is_ta():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def __str__(self):
        return '[' + str(self.published_date.strftime("%b %d %Y %H:%M:%S")) + '] ' + self.title

    class Meta:
        unique_together = ['title', 'text']


class Content_KhaledAbdulaziz(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    published_date = models.DateTimeField(auto_now=True, editable=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @staticmethod
    def is_ta_KhaledAbdulaziz():
        return True

    @staticmethod
    def is_ta_scraped():
        return True

    @staticmethod
    def is_ta():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def __str__(self):
        return '[' + str(self.published_date.strftime("%b %d %Y %H:%M:%S")) + '] ' + self.title

    class Meta:
        unique_together = ['title', 'text']


class Content_alanmasters(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    published_date = models.DateTimeField(auto_now=True, editable=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @staticmethod
    def is_ta_alanmasters():
        return True

    @staticmethod
    def is_ta_scraped():
        return True

    @staticmethod
    def is_ta():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def __str__(self):
        return '[' + str(self.published_date.strftime("%b %d %Y %H:%M:%S")) + '] ' + self.title

    class Meta:
        unique_together = ['title', 'text']


class Content_CryptoNTez(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    published_date = models.DateTimeField(auto_now=True, editable=True)
    has_been_sent_to_telegram = models.BooleanField(default=False)
    has_been_sent_to_telegram_for_unsubscribed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    @staticmethod
    def is_ta_cryptontez():
        return True

    @staticmethod
    def is_ta_scraped():
        return True

    @staticmethod
    def is_ta():
        return True

    def __lt__(self, other):
        return self.published_date > other.published_date

    def __str__(self):
        return '[' + str(self.published_date.strftime("%b %d %Y %H:%M:%S")) + '] ' + self.title

    class Meta:
        unique_together = ['title', 'text']


class Fear_and_Greed_Index(models.Model):
    value = models.IntegerField()
    value_classification = models.CharField(max_length=128)
    update_time = models.DateTimeField()

    def __str__(self):
        return '[' + str(self.update_time) + '] ' + str(self.value)
