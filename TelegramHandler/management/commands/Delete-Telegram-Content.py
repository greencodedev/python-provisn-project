from django.core.management import BaseCommand
import logging
from TelegramHandler.models import ContentCoinDesk


LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger.info('Deleting all Telegram messages...')
        objects = ContentCoinDesk.objects.all()
        for object in objects:
            object.delete()
        logger.info('Done deleting all Telegram messages!')
