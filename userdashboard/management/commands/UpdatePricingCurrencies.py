from django.core.management import BaseCommand
from userdashboard.models import Currency_Value


class Command(BaseCommand):
    help = "Updates the current prices for cryptocurrencies which are used for payments"

    def handle(self, *args, **kwargs):
        try:
            btc_pricing = Currency_Value(
                currency='BTC'
            )
            btc_pricing.save()
            eth_pricing = Currency_Value(
                currency='ETH'
            )
            eth_pricing.save()
        except Exception as exc:
            print("###########################################")
            print("MASSIVE EXCEPTION OCCURRED IN PRICE UPDATER")
            print(exc)
            print("###########################################")
