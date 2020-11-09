from django.core.management.base import BaseCommand
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from userdashboard.models import Beam, \
    BlockchainNew, \
    BlockchainEvent, \
    ArtificialIntelligence, \
    TechnicalAnalysi, \
    TokenWatchlist
from TelegramHandler.models import TelegramAccountWrapper, \
    TelegramActiveUsersBroadcast, \
    TelegramActiveUsersChat, \
    ContentCoinDesk
from ContentScraper.models import *
from django.utils import timezone
from django.template.defaultfilters import linebreaksbr
from time import sleep
from django.contrib.humanize.templatetags.humanize import naturaltime
import re
from plutus.settings import TELEGRAM_BOT_TOKEN


LOGLEVEL = logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGLEVEL)

logger = logging.getLogger(__name__)

# Test Bot
#TOKEN = '836327421:AAFrXFEZOYywPPH_oeiOhSk_egHMznafjR8'
# Dev Bot
TOKEN = TELEGRAM_BOT_TOKEN

# AI Test Channel
#AI_GROUP_CHAT_ID = -1001213780453
# Actual AI Channel
AI_GROUP_CHAT_ID = -1001175987244

# DcPacky Private Chat
#AI_CONFIRMATION_CHAT_ID = 865599123
# Provisn Core Chat
AI_CONFIRMATION_CHAT_ID = -267400320

UNSUB_BROADCAST_GROUP_CHAT_ID = -1001431253444
SUB_BROADCAST_GROUP_CHAT_ID = -1001436766141
SUB_CHAT_GROUP_ID = -1001397972780

TIMEDELTA_HOUR_VALUE = 5

updater = Updater(TOKEN, use_context=True)

def cleanhtml(raw_html):
  cleanr = re.compile('<img.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def prepareText(content, date, subscribed):
    send_text = content

    if subscribed:
        send_text += '\n<b>' + naturaltime(date) + '</b>'
    else:
        send_text += '\n' + naturaltime(date) + \
                 '\n\n<b>Get this advice and more even quicker on:</b> <a href="https://provisn.com/">PROVISN.com</a>'

    ### Remove unwanted HTML Tags or an error occurs!
    send_text = send_text.replace('<p>', '')
    send_text = send_text.replace('</p>', '')
    send_text = send_text.replace('<u>', '')
    send_text = send_text.replace('</u>', '')
    send_text = send_text.replace('<br>', '\n')
    send_text = send_text.replace('</br>', '\n')
    send_text = send_text.replace('<br/>', '\n')
    send_text = send_text.replace('<br />', '\n')
    send_text = send_text.replace('&nbsp;', ' ')
    send_text = send_text.replace('<div>', '')
    send_text = send_text.replace('</div>', '')
    if 'div' in send_text:
        clean = re.compile('<.*?>')
        send_text = re.sub(clean, '', send_text)
    send_text = cleanhtml(send_text)
    return send_text


def sendOutObjects(unsentObjects, context, subscribed, ChannelName):
    for i in range(0, len(unsentObjects)):
        logger.info('Sending out for channel: {}'.format(ChannelName))
        content = unsentObjects[i].text
        ### Get post content and add date
        if ChannelName == 'Beams':
            content = unsentObjects[i].text + \
                        '\n\n<b>Targets</b>: ' + unsentObjects[i].targets + \
                        '\n\n<b>Stop-Loss</b>: ' + unsentObjects[i].stop_loss + \
                        '\n\n<b>Notes</b>: ' + unsentObjects[i].notes
        try:
            send_text = '<b>PROVISN Telegram Ticker ' + ChannelName + ' </b>\n\n\n' + \
                    prepareText(content, unsentObjects[i].published_date, subscribed)
        except:
            send_text = '<b>PROVISN Telegram Ticker &#62; ' + ChannelName + ' &#60;</b>\n\n\n' + \
                        prepareText(content, unsentObjects[i].published_date, subscribed)

        ### Send message to channel
        if subscribed:
            context.bot.send_message(chat_id=SUB_BROADCAST_GROUP_CHAT_ID,
                                        text=send_text, parse_mode=telegram.ParseMode.HTML)
            unsentObjects[i].has_been_sent_to_telegram = True
        else:
            context.bot.send_message(chat_id=UNSUB_BROADCAST_GROUP_CHAT_ID,
                                        text=send_text, parse_mode=telegram.ParseMode.HTML)
            unsentObjects[i].has_been_sent_to_telegram_for_unsubscribed = True
        unsentObjects[i].save()

        ### Wait to prevent the bot being timeouted
        sleep(5)


def callback_new_member_check(bot, update):
    if bot.message.chat_id != SUB_BROADCAST_GROUP_CHAT_ID and bot.message.chat_id != SUB_CHAT_GROUP_ID:
        return
    logger.info('New members!')
    for user in bot.message.new_chat_members:
        user_id = user.id
        from_usr = user.name
        try:
            telegram_wrapper_objects = TelegramAccountWrapper.objects.get(telegram_name=from_usr)
            logger.info(telegram_wrapper_objects)
            if telegram_wrapper_objects.account.userLevel is 0:
                raise Exception
            print('Auth successful, adding new user to DB')
            if bot.message.chat_id == SUB_BROADCAST_GROUP_CHAT_ID:
                NewActiveUserObject = TelegramActiveUsersBroadcast(
                    Wrapper=telegram_wrapper_objects,
                    User_Id = user_id
                )
                NewActiveUserObject.save()
            elif bot.message.chat_id == SUB_CHAT_GROUP_ID:
                NewActiveUserObject = TelegramActiveUsersChat(
                    Wrapper=telegram_wrapper_objects,
                    User_Id=user_id
                )
                NewActiveUserObject.save()

        except Exception as exc:
            bot.message.delete()
            logger.info('No account wrapper found for user or user has no subscription!')
            updater.bot.kick_chat_member(SUB_BROADCAST_GROUP_CHAT_ID, user_id)
            updater.bot.kick_chat_member(SUB_CHAT_GROUP_ID, user_id)
            updater.bot.send_message(user_id, 'You have been kicked from the group, cause you either have no PROVISN Subscription or yours has run out!')
            logger.warning(exc)
            logger.info('Kicked unrecognized user: ' + from_usr)

    bot.message.delete()
    logger.info('New members End!')


def callback_left_member_check(bot, update):
    bot.message.delete()

def callback_check_for_unsubscribed_users(context: telegram.ext.CallbackContext):
    logger.info('Checking for unsubscribed users!')

    ## Broadcast Sub Channel
    activeTelegramUsersBroadcast = TelegramActiveUsersBroadcast.objects.filter(Wrapper__account__userLevel=0)
    for user in activeTelegramUsersBroadcast:
        updater.bot.kick_chat_member(SUB_BROADCAST_GROUP_CHAT_ID, user.User_Id)
        print('Kicked: ' + user.Wrapper.telegram_name)
        user.delete()

    ## Sub Chat Channel
    activeTelegramUsersChat = TelegramActiveUsersChat.objects.filter(Wrapper__account__userLevel=0)
    for user in activeTelegramUsersChat:
        updater.bot.kick_chat_member(SUB_CHAT_GROUP_ID, user.User_Id)
        print('Kicked: ' + user.Wrapper.telegram_name)
        user.delete()


def callback_minute_subscribed(context: telegram.ext.CallbackContext):
    logger.info('Subscribed Content Check')
    unsentAIObjects = ArtificialIntelligence.objects.filter(has_been_sent_to_telegram=False).filter(
        published_date__lte=(timezone.now()), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentAIObjects, context, True, 'A.I. Signal Calls')

    unsentBeamObjects = Beam.objects.filter(has_been_sent_to_telegram=False).filter(
        published_date__lte=(timezone.now()), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentBeamObjects, context, True, 'Beams')

    unsentNewsObjects = BlockchainNew.objects.filter(has_been_sent_to_telegram=False).filter(
        published_date__lte=(timezone.now()), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentNewsObjects, context, True, 'News')

    unsentTAObjects = TechnicalAnalysi.objects.filter(has_been_sent_to_telegram=False).filter(
        published_date__lte=(timezone.now()), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentTAObjects, context, True, 'Technical Analysis')

    unsent_content_telegram_coin_desk = ContentCoinDesk.objects.filter(has_been_sent_to_telegram=False,
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_telegram_coin_desk, context, True, 'News')



    ## Trading View TAs

    unsent_content_tv_khaled = Content_KhaledAbdulaziz.objects.filter(
        has_been_sent_to_telegram=False,
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_khaled, context, True, 'Technical Analysis')

    unsent_content_tv_faibik = Content_Faibik.objects.filter(
        has_been_sent_to_telegram=False,
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_faibik, context, True, 'Technical Analysis')

    unsent_content_cryptontez = Content_CryptoNTez.objects.filter(
        has_been_sent_to_telegram=False,
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_cryptontez, context, True, 'Technical Analysis')

    unsent_content_alanmasters = Content_alanmasters.objects.filter(
        has_been_sent_to_telegram=False,
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_alanmasters, context, True, 'Technical Analysis')




def callback_minute_unsubscribed(context: telegram.ext.CallbackContext):
    logger.info('Unsubscribed content check!')
    ### Get unsent content, older than 3 hours and not marked as sent yet
    unsentAIObjects = ArtificialIntelligence.objects.filter(has_been_sent_to_telegram_for_unsubscribed=False)\
        .filter(published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentAIObjects, context, False, 'A.I. Signal Calls')

    unsentBeamObjects = Beam.objects.filter(has_been_sent_to_telegram_for_unsubscribed=False)\
        .filter(published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentBeamObjects, context, False, 'Beams')

    unsentNewsObjects = BlockchainNew.objects.filter(has_been_sent_to_telegram_for_unsubscribed=False)\
        .filter(published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentNewsObjects, context, False, 'News')

    unsentTAObjects = TechnicalAnalysi.objects.filter(has_been_sent_to_telegram_for_unsubscribed=False)\
        .filter(published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsentTAObjects, context, False, 'Technical Analysis')

    unsent_content_telegram_coin_desk = ContentCoinDesk.objects.filter(has_been_sent_to_telegram_for_unsubscribed=False,
                                                                       published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_telegram_coin_desk, context, False, 'News')

    unsent_content_tv_khaled = Content_KhaledAbdulaziz.objects.filter(
        has_been_sent_to_telegram_for_unsubscribed=False,
        published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_khaled, context, False, 'Technical Analysis')

    unsent_content_tv_faibik = Content_Faibik.objects.filter(
        has_been_sent_to_telegram_for_unsubscribed=False,
        published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)), published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_faibik, context, False, 'Technical Analysis')

    unsent_content_tv_cryptontez = Content_CryptoNTez.objects.filter(
        has_been_sent_to_telegram_for_unsubscribed=False,
        published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)),
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_cryptontez, context, False, 'Technical Analysis')

    unsent_content_tv_alanmasters = Content_alanmasters.objects.filter(
        has_been_sent_to_telegram_for_unsubscribed=False,
        published_date__lte=(timezone.now() - timezone.timedelta(hours=TIMEDELTA_HOUR_VALUE)),
        published_date__gte=(timezone.now() - timezone.timedelta(days=1)))
    sendOutObjects(unsent_content_tv_alanmasters, context, False, 'Technical Analysis')


def start(update: updater, context: CallbackContext):
    """Send a message when the command /start is issued."""

    # ToDo Update Welcome Message
    update.message.reply_text("Hello fellow Provisn user!\nWe're happy to see you in our Telegram Channel.")


def login(update: updater, context:CallbackContext):
    return
    update.message.reply_text("Logging you in...")
    if update.effective_message.chat_id < 0:
        return
    login_token = update.effective_message.text.replace('/login ', '')
    from django.core.exceptions import ObjectDoesNotExist
    try:
        LoginObject = TelegramAccountWrapper.objects.get(token=login_token)
        LoginObject.telegram_name = update.effective_message.from_user['username']
        LoginObject.save()
        update.message.reply_text('Token Confirmed! But login not yet implemented...')

    except ObjectDoesNotExist as ODNEexc:
        update.message.reply_text("Sorry, couldn't verify you! Please try again")


def help(update: updater, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: updater, context: CallbackContext):
    logger.info('Message Received!')
    #print(str(type(update.effective_message.chat_id)) + ' - ' + str(update.effective_message.chat_id) + ' - ' + str(GROUP_CHAT_ID) + ' - ' + str(update.effective_message.chat_id == GROUP_CHAT_ID))
    if update.effective_message.chat_id != AI_GROUP_CHAT_ID:
        return
    """Creating AI Object"""
    #user = get_user_model()
    text = linebreaksbr(update.effective_message.text)
    text = text.replace('Question:<br>', '')
    text = text.replace('Pairing', '<strong>Pairing</strong>')
    text = text.replace('Call', '<strong>Call</strong>')
    text = text.replace('Indicator', '<strong>Indicator</strong>')
    text = text.replace('Question:', '<strong>Question:</strong>')
    text = text.partition('Tier:')[0]

    if 'Indicator' not in text:
        print('Not an Indicator Message received! Ignoring')
        return

    newAI = ArtificialIntelligence(
        text = text,
        published_date=timezone.now()
    )
    newAI.save()
    """ Uncomment the following if you want to reply to the received msg"""
    #update.effective_message.reply_text('Confirmed!')
    updater.bot.send_message(AI_CONFIRMATION_CHAT_ID, 'Successfully added AI Message: ' + str(newAI.id))



class Command(BaseCommand):
    help = "Provisn.com Telegram Bot"


    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.


    def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)



    def handle(self, *args, **kwargs):
        print('Telegram Bot Starting...')
        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("login", login))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, callback_new_member_check))
        dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, callback_left_member_check))


        ### Automatic Broadcast Handler
        job_queue_sub = updater.job_queue
        job_queue_unsub = updater.job_queue

        job_queue_subscription_check = updater.job_queue

        job_minute_sub = job_queue_sub.run_repeating(callback_minute_subscribed, interval=60, first=0)
        job_minute_unsub = job_queue_unsub.run_repeating(callback_minute_unsubscribed, interval=300, first=0)

        subscription_check = job_queue_subscription_check.run_repeating(callback_check_for_unsubscribed_users, interval=30, first=0)

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()
        print('PROVISN Telegram Bot running!')

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
