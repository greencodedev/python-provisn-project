from django.core.management.base import BaseCommand
from ...models import *
from fileReader import load_discord_obj
from django.utils import timezone
from django.contrib.auth import get_user_model
from ...views import createContentPageObject
from bleach import linkify
from django.template.defaultfilters import linebreaksbr
from django.utils.dateparse import parse_datetime
from datetime import datetime


Channel = ['beams', 'blockchain_events', 'breaking_news', 'market_intuition', 'member_perks', 'plutus_ai', 'technical_analysis', 'token_watchlist']
Models = [Beam, BlockchainEvent, BlockchainNew, MarketIntuition, MemberPerk, ArtificialIntelligence, TechnicalAnalysi, TokenWatchlist]

class Command(BaseCommand):
    help = "Imports the discord messages from their files into the according models"

    def handle(self, *args, **kwargs):
        print("Starting Message importer...")
        for i in range(len(Channel)):
            print('Starting for ' + Channel[i])

            discordObject = createContentPageObject(Channel[i])
            for j in range(0, len(discordObject)):
                content = (discordObject[j]['content'])
                #Experimental
                content = '<br/>'.join(content.split('\n'))
                content = linkify(content)
                dt = datetime.strptime(discordObject[j]['time'], '%Y-%m-%d %H:%M:%S')
                print(str(dt) + "|" + discordObject[j]['time'])
                try:
                    currObject = Models[i](text = content,
                                       created_date = dt,
                                       published_date = dt,
                                       author = get_user_model().objects.all()[0],
                                       title = '')
                except TypeError:
                    currObject = Models[i](text=content,
                                           created_date=dt,
                                           published_date=dt)
                currObject.save()

        print('Done')
