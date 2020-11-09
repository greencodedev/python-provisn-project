from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Converts Ethereum prices to the values for the pricecheck in receivers.py'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=float)

    def handle(self, *args, **kwargs):
        amount = kwargs['amount']
        print("Input: " + str(amount))
        newAmount = (amount * (10 ** 18))
        print("Please add: " + str(format(newAmount, '.0f')))