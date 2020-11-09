from django.core.management import BaseCommand
from plutus.settings import TWITTER_ACCESS_TOKEN_KEY, \
    TWITTER_ACCESS_TOKEN_SECRET, \
    TWITTER_CONSUMER_KEY, \
    TWITTER_CONSUMER_SECRET
import twitter
from TwitterHandler.models import Tweet
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
from django.db.utils import IntegrityError
from bleach import linkify


class Command(BaseCommand):
    help = "Twitter Bot which handles all twitter stuff"

    api = twitter.Api(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token_key=TWITTER_ACCESS_TOKEN_KEY,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )

    def handle(self, *args, **kwargs):
        timeline = self.api.GetHomeTimeline(count=200)
        print(timeline)
        for tweet in timeline:
            print('User: ' + tweet.user.name)
            print('Text: ' + tweet.text)
            for url in tweet.urls:
                print('URLs: ' + url.url)
            print('DateTime: ' + tweet.created_at)
            print('\n')
            dt = datetime.fromtimestamp(tweet.created_at_in_seconds)
            text = linkify(tweet.text)
            newModel = Tweet(
                user=tweet.user.name,
                text=text,
                published_date=dt,
                tweet_id=tweet.id
            )
            try:
                newModel.save()
            except IntegrityError:
                ## Is thrown if tweet is already in DB
                pass


