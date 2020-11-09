from django.core.management import BaseCommand
from ContentScraper.utils import get_fear_and_greed_data
from ContentScraper.models import Fear_and_Greed_Index
from django.utils.timezone import now
import logging

LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger.info('Updating Fear and Greed Index')
        data = get_fear_and_greed_data()['data'][0]
        fgi = Fear_and_Greed_Index(
            value=data['value'],
            value_classification=data['value_classification'],
            update_time=now()
        )
        fgi.save()
        logger.info('Done Updating Fear and Greed Index')