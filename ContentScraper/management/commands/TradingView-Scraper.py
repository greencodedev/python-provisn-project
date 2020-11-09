import urllib.request
from bs4 import BeautifulSoup
import logging

from django.core.management import BaseCommand
from django.db import IntegrityError

from ContentScraper.models import *
import json
from time import sleep

LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "PROVISN TradingView Scraper"

    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)

    def handle(self, *args, **kwargs):
        logger.info('Starting TradingView Scraper')

        self.KhaledAbdulaziz()
        sleep(5)
        self.Faibik()
        sleep(5)
        self.alanmasters()
        sleep(5)
        self.CryptoNTez()

        logger.info('TradingView Scraper Done')


    def KhaledAbdulaziz(self):
        logger.info('Khaled')
        url = 'https://www.tradingview.com/u/KhaledAbdulaziz/'
        self.get_content(url, Content_KhaledAbdulaziz)

    def Faibik(self):
        logger.info('Faibik')
        url = 'https://www.tradingview.com/u/Faibik/'
        self.get_content(url, Content_Faibik)

    def get_content(self, url, model):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        request = urllib.request.Request(url, headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('a',
                              attrs={'class': 'tv-widget-idea__title apply-overflow-tooltip js-widget-idea__popup'},
                              href=True)

        urls = []
        for link in links:
            url = link['href']
            urls.append('https://www.tradingview.com' + url)

        for url in urls:
            request = urllib.request.Request(url, headers={'User-Agent': user_agent})
            html = urllib.request.urlopen(request).read()
            soup = BeautifulSoup(html, 'html.parser')

            title_class = 'tv-chart-view__title-name'
            title = soup.find('h1', attrs={'class': title_class}, ).get_text()

            content_text_class = 'tv-chart-view__description'
            content = soup.find('div', attrs={'class': content_text_class}, ).decode_contents()

            diagram_class = 'tv-card-social-item apply-common-tooltip tv-card-social-item--agrees tv-card-social-item--button tv-card-social-item--border tv-social-row__item'
            diagram = soup.find('span', attrs={'class': diagram_class}, )

            diagram_id = diagram['data-image_url']
            image = "https://www.tradingview.com/i/" + diagram_id

            title = str(title)

            # content = content.replace('<div class="tv-chart-view__description selectable">', '')
            # content.replace('<span class="tv-chart-view__tag-page-link">', '')
            # content.replace('</span>', '')
            soup = BeautifulSoup(content, 'html.parser')
            for a_tag in soup.findAll('a'):
                a_tag.unwrap()
            for span_tag in soup.findAll('span'):
                span_tag.unwrap()

            content = soup.decode_contents()
            content = content[:content.find('<br/>\n<br/>')]
            try:
                new_content = model(
                    title=title,
                    text=content,
                    image_url=image,
                    url=url
                )

                new_content.save()
            except IntegrityError:
                pass

    def alanmasters(self):
        logger.info('alanmasters')
        url = 'https://www.tradingview.com/u/alanmasters/'
        self.get_content(url, Content_alanmasters)

    def CryptoNTez(self):
        logger.info('CryptoNTez')
        url = 'https://www.tradingview.com/u/CryptoNTez/'
        self.get_content(url, Content_CryptoNTez)

