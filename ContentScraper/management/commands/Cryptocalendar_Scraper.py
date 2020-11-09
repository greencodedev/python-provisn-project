import logging
import urllib
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from userdashboard.models import BlockchainEvent
from datetime import datetime
from django.utils.timezone import now
from django.db.utils import IntegrityError


LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    url = 'https://cryptocalendar.pro/'

    def handle(self, *args, **kwargs):
        logger.info('Updating Cryptocalendar.pro')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        request = urllib.request.Request(self.url, headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')
        link_container = soup.find_all('div', attrs={'class': 'event-block'})
        for event in link_container:
            a_tag = event.find('a')
            event_url = 'https://cryptocalendar.pro' + a_tag['href']
            request = urllib.request.Request(event_url, headers={'User-Agent': user_agent})
            html = urllib.request.urlopen(request).read()
            soup = BeautifulSoup(html, 'html.parser')
            event_title = soup.find('h1').text
            event_title = event_title.replace('  ', '').replace('\n', '')
            event_description = soup.find('div', {'class': 'col-lg-12'}).text
            event_description = event_description.replace('  ', '').replace('\n', '')
            event_date = soup.find('time').text
            event_date_parsed = datetime.strptime(event_date, '%d.%m.%Y')
            new_event = BlockchainEvent(
                title=event_title,
                text=event_description,
                date_of_event=event_date_parsed,
                published_date=now(),
                color_class='indicator-red'
            )
            try:
                ev = new_event.save()
            except IntegrityError:
                'Content already added!'
                pass
            print('added')



        logger.info('Done Updating Cryptocalendar.pro')



