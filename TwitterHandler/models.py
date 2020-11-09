from django.db import models


# Create your models here.
class Tweet(models.Model):
    user = models.CharField(max_length=50)
    text = models.TextField()
    published_date = models.DateTimeField()
    isTweet = models.BooleanField(default=True)
    tweet_id = models.BigIntegerField()

    def __str__(self):
        return str(self.user) + ' - Tweeted: ' + self.text

    def __lt__(self, other):
        return self.published_date > other.published_date

    class Meta:
        unique_together = ['user', 'text', 'published_date']
