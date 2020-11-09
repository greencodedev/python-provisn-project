from django.core.management import BaseCommand
import logging; logging.basicConfig(level=logging.ERROR)
from telethon import TelegramClient, events


api_id = 180552
api_hash = '5f5781fcf26a0daae71e4c37afbedee6'

cindicator_bot_id = 452828527
cryptometer_bot_id = 498989457

dez_id = 549115004

# unused since we will be testing other channels
channel_url = 'https://t.me/joinchat/AAAAAEYYJCw_Z5StV-7ZBQ'

class Command(BaseCommand):
    from telethon import TelegramClient, events
    from telethon.tl.types import UpdateShortMessage, PeerUser, InputPeerChannel, UpdateNewMessage, UpdateShort, \
        UpdateShortChatMessage
    from telethon.tl.functions.messages import ForwardMessagesRequest

    client = TelegramClient('session_name', api_id, api_hash)  # , update_workers=2, spawn_read_thread=False)
    client.start()

    @client.on(events.NewMessage)
    def my_event_handler(self, event):
        if cindicator_bot_id == event.message.from_id:
            print("got a message from cindicator bot!")
            # from_entity = client.get_entity("https://t.me/CindicatorBot")
            to_entity = self.client.get_input_entity("https://t.me/joinchat/AAAAAEYYJCw_Z5StV-7ZBQ")
            print("trying to forward message to cnd channel")
            self.client.forward_messages(
                to_entity,
                event.message
            )

        if cryptometer_bot_id == event.message.from_id:
            print("got a message from cryptometer bot!")
            # from_entity = client.get_entity("https://t.me/CryptometerBot")
            to_entity = self.client.get_input_entity("https://t.me/joinchat/AAAAAFBWleABC4A7Z6HNHQ")
            print("trying to forward message to cryp channel")
            self.client.forward_messages(
                to_entity,
                event.message
            )

        # DEBUGGING
        # if dez_id == event.message.from_id:
        #   print("got a message from dez!")
        #   # from_entity = client.get_entity("https://t.me/dezmathio")
        #   to_entity = client.get_entity("https://t.me/joinchat/AAAAAFBWleABC4A7Z6HNHQ")
        #   # msgs = [messages] # prob unnecessary
        #   # msg_id = event.message.id
        #   print("trying to forward message to cryp channel")

        #   client.forward_messages(
        #     to_entity,
        #     event.message
        #   )

        if 'Indicator' in event.raw_text:
            print("Event coming through where it has raw_text containing Indicator")
            print("~~~~~ Start of NewMessage stringify ~~~~~")
            print(event.stringify())
            print("~~~~~ End of NewMessage stringify ~~~~~")

        # events.UpdateShortMessage

        # UpdateShortMessage(
        #   out=False,
        #   mentioned=False,
        #   media_unread=False,
        #   silent=False,
        #   id=5244,
        #   user_id=549115004,
        #   message='Another test',
        #   pts=8742,
        #   pts_count=1,
        #   date=datetime.utcfromtimestamp(1522539286),
        #   fwd_from=None,
        #   via_bot_id=None,
        #   reply_to_msg_id=None,
        #   entities=[
        #   ]
        # )

        # ChatAction
        # MessageEdited
        # MessageDeleted
        # MessageRead
        # NewMessage
        # Raw
    def handle(self, *args, **kwargs):
            print("Started to watch messages")

            self.client.idle()
