# import logging
# logger = logging.getLogger('myapp')
# hdlr = logging.FileHandler('/var/tmp/myapp.log')
# logger.addHandler(hdlr)
# logger.setLevel(logging.DEBUG)
from telethon import TelegramClient, events

# david
api_id = 180552
api_hash = '5f5781fcf26a0daae71e4c37afbedee6'
# phone 18054556981


#DcP
#api_id = 865426
#api_hash = 'cd826b6860816e3dedfc19d61b1eb9bd'
#dcpacky_id = 865599123

# dez
# api_id = '73681'
# api_hash = 'ccc8f4221549f109db6e166f08a1d6a2'

# User CindicatorBot @CindicatorBot (#452828527):
# User Cryptometer @CryptometerBot (#498989457):


cindicator_bot_id = 452828527
cryptometer_bot_id = 498989457

# cryptometer_bot_id = 498989457
# cryptometer_bot_id = 129782279
# Cindicator Test
#DcPackyDevBot
#cindicator_bot_id = 865599123

# real channel
#channel_url = 'https://t.me/joinchat/HaeSp0U5CVqq5AErQklOKQ'
# Real Channel ID
#channel = 1175987244
channel = -1001175987244

#channel_id = -1001213780453

# test channel
# channel_url = 'https://t.me/joinchat/AAAAAE1pixPkrVx5thuseA'


with TelegramClient('session_name', api_id, api_hash) as client:

    @client.on(events.NewMessage())
    async def fwder(event):
        if event.message.sender_id == cindicator_bot_id:
            print(event.stringify())
        elif event.message.sender_id == cryptometer_bot_id:
            print(event.stringify())

        if event.message.sender_id == cindicator_bot_id:
            print("Forwarding message to channel from cindicator")
            await messageChannel(event)
            print('###DONE###')
            return
        elif event.message.sender_id == cryptometer_bot_id:
            print("Forwarding message to channel from cryptometer")
            await messageChannel(event)
            print('###DONE###')
            return

        print("FW normal update")


    async def messageChannel(event):
        print('###messageChannel###')
        #channel = 862521165#await client.get_entity(channel_url)
        #from_entity = event._chat_peer.user_id#bot
        to_entity = channel #await client.get_input_entity(channel)
        #events = [event]
        print('###messageChannel FORWARDING###')
        await event.message.forward_to(to_entity)
        print('###messageChannel DONE###')

    print('Start run')
    client.run_until_disconnected()
