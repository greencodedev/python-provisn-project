from django.core.management.base import BaseCommand
from userdashboard.models import BlockchainEvent

### This application checks all Trial or Subscription users, if their subscription is still running and
### sets it to userLevel 0 if necessary

class Command(BaseCommand):
    help = "Checks all users if their subscription has run out"

    def handle(self, *args, **kwargs):
        print('Start Renaming...')
        events_to_be_changed = BlockchainEvent.objects.filter(color_class='indicator-yellow')
        for event in events_to_be_changed:
            event.color_class = 'event_color_brown'
            event.save()
        events_to_be_changed = BlockchainEvent.objects.filter(color_class='bg-success')
        for event in events_to_be_changed:
            event.color_class = 'event_color_blue'
            event.save()
        print('Done')