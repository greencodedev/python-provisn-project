from django.core.management import BaseCommand
import os
from plutus.settings import MEDIA_ROOT
from userdashboard.models import Coin


class Command(BaseCommand):
    help = "Imports all crypto currency icons from images"

    def handle(self, *args, **kwargs):
        directory = MEDIA_ROOT + '/coin_icons/'

        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                coin_name = filename.replace('.png', '')
                file = '/coin_icons/' + filename
                print(filename)
                print(coin_name)
                print(file)
                print()
                new_coin = Coin(
                    name=coin_name.upper(),
                    short_name=coin_name.upper(),
                    coin_icon=file
                )
                new_coin.save()
                continue
            else:
                continue
