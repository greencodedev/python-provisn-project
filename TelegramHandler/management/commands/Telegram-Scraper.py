import datetime
from urllib.parse import urlparse

from django.utils import timezone
import logging
from django.template.defaultfilters import linebreaksbr
from django.core.management import BaseCommand
from django.db import IntegrityError
from telethon import TelegramClient
from TelegramHandler.models import ContentCoinDesk
from bleach.linkifier import Linker
from plutus.settings import TELEGRAM_PHONE_NUMBER, \
    TELEGRAM_API_ID, \
    TELEGRAM_NAME, \
    TELEGRAM_API_HASH, \
    DEBUG
from bs4 import BeautifulSoup
from time import sleep
from django.utils.html import mark_safe

LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)
logger = logging.getLogger(__name__)

def set_target(attrs, new=False):
    p = urlparse(attrs[(None, 'href')])
    if p.netloc not in ['my-domain.com', 'other-domain.com']:
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'class')] = 'external'
    else:
        attrs.pop((None, 'target'), None)
    return attrs

class Command(BaseCommand):
    help = "PROVISN Telegram Bot"

    phone_number = TELEGRAM_PHONE_NUMBER
    api_id = TELEGRAM_API_ID
    api_hash = TELEGRAM_API_HASH
    name = TELEGRAM_NAME

    linker = Linker(callbacks=[set_target])

    if DEBUG:
        phone_number = '4917631653701'
        api_id = 865426
        api_hash = 'cd826b6860816e3dedfc19d61b1eb9bd'
        name = 'DcPacky'

    message_amount = 30

    client = TelegramClient(name, api_id, api_hash)
    client.connect()

    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)

    def get_messages(self, chat, model, tag, *args, **kwargs):
        with self.client:
            i = 0
            for message in self.client.iter_messages(chat):
                i += 1
                if i == self.message_amount:
                    break
                try:
                    text = '' + message.text

                    text = self.linker.linkify(text)

                    if 'strip_a' in kwargs:
                        soup = BeautifulSoup(text, 'html.parser')
                        soup.select_one('a').decompose()
                        text = str(soup)

                    text = linebreaksbr(text)

                    if 'strip_a' in kwargs:
                        text = text.replace('[​​]( ', '')
                        text = text.replace('[​​](\n', '')
                        text = text.replace('[​​](', '')

                    text = text.replace('&quot;', '"')
                    text = text.replace('&lt;', '<')
                    text = text.replace('&gt;', '>')

                    title = text.partition('<br>')[0]
                    if '<a' in title:
                        title = ''


                    new_content = model(
                        title=title,
                        text=text,
                        # published_date as in post
                        # published_date=message.date.replace(tzinfo=None)
                        published_date=timezone.now(),
                    )
                    new_content.save()
                    new_content.tags.add(tag)
                    print("Added!")
                except IntegrityError:
                    print('Content Already Existing')
                    pass
                except TypeError:
                    pass


    def handle(self, *args, **kwargs):
        logger.info('Start Scraping Messages')

        #logger.info('Daily HODL')
        #self.get_messages('thedailyhodl', ContentDailyHodl, 'DailyHODL')
        #sleep(5)

        logger.info('Coin Desk')
        self.get_messages('coindesk_news', ContentCoinDesk, 'CoinDesk')
        sleep(5)

        #logger.info('Coin Telegraph')
        #self.get_messages('cointelegraph', ContentCoinTelegraph, 'CoinTelegraph', strip_a=True)
        #sleep(5)

        #logger.info('Bitcoinist')
        #self.get_messages('bitcoinistnews', ContentBitcoinist, 'Bitcoinist')

        logger.info("Done Scraping Messages")

