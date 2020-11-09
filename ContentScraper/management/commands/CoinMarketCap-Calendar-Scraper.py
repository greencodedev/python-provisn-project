import logging
import urllib
import datetime
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.db import IntegrityError
from userdashboard.models import BlockchainEvent
from time import sleep, time
from django.utils.timezone import now
from plutus.settings import DEBUG

LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "PROVISN CoinMarketCap Calendar Scraper"

    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)

    def handle(self, *args, **kwargs):
        logger.info('Starting Coin Market Cap Event Scraper')

        self.get_content('https://coinmarketcap.com/events/', BlockchainEvent)

        logger.info('Finished Coin Market Cap Event Scraping')


    def get_content(self, url, model):
        if DEBUG:
            start_time = time()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        request = urllib.request.Request(url, headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')

        link_container = soup.find_all('div', attrs={'class': 'cal-event'})
        for event in link_container:
            link = event.findChild('div', attrs={'class': 'cal-event__name'}, recursive=True).findChild('a', recursive=False)
            event_url = 'https://coinmarketcap.com' + link['href']

            request = urllib.request.Request(event_url, headers={'User-Agent': user_agent})
            html = urllib.request.urlopen(request).read()
            soup = BeautifulSoup(html, 'html.parser')

            # event_name = soup.find('div', attrs={'class': 'header'}).findChild('h1', recursive=False).text
            event_name = soup.find('div', attrs={'class': 'cal-event-detail'}).findChild('img', recursive=False).attrs['alt']
            event_date = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[0].findChildren('div', recursive=False)[1].text

            # partition_strings = ['\n-\n', '\n -\n']
            # for string in partition_strings:
            #     event_start_date = event_date.partition(string)[0]
            #     event_end_date = event_date.partition(string)[2]
            #     try:
            #         event_start_date = datetime.datetime.strptime(event_start_date, '\n%b %d, %Y')
            #         event_end_date = datetime.datetime.strptime(event_end_date, '%b %d, %Y\n')
            #         break
            #     except Exception as ex:
            #         continue

            partition_strings = event_date.split(" - ")
            event_start_date = partition_strings[0]
            event_end_date = partition_strings[1]
            try:
                event_start_date = datetime.datetime.strptime(event_start_date, '%b %d, %Y')
                event_end_date = datetime.datetime.strptime(event_end_date, '%b %d, %Y')
                # break
            except Exception as ex:
                continue
            if DEBUG:
                print('Start Time taken: ' + str(event_start_date))
            info_length = len(soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'}))

            details = venue = location = event_info_url = ""
            for i in range(0, info_length):
                current_area = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[i].findChildren('div', recursive=False)[0].text
                if current_area == ' Dates:':
                    continue
                elif current_area == ' Details:':
                    details = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[i].findChildren('div', recursive=False)[1].text
                elif current_area == ' Venue:':
                    venue = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[i].findChildren('div', recursive=False)[1].text
                elif current_area == ' Location:':
                    location = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[i].findChildren('div', recursive=False)[1].text
                elif 'For more information:' in current_area:
                    event_info_url = soup.find('div', attrs={'class': 'cal-event-detail'}).findAll('div', attrs={'class': 'cmc-bottom-margin-1x'})[i].findChildren('div', recursive=False)[1].text
                else:
                    logger.error("Unrecognized Information Block!")

            new_content = BlockchainEvent(
                title=event_name,
                date_of_event=event_start_date,
                text=details,
                venue=venue,
                location=location,
                event_url=event_info_url,
                published_date=now(),
                color_class='event_color_brown'
            )
            try:
                new_content.save()
                logger.info('Saved Content')
            except IntegrityError as ie:
                logger.warning('Content already existing!')
                pass

            sleep(5)
        if DEBUG:
            end_time = time()
            print('Time taken: ' + str(end_time - start_time))
