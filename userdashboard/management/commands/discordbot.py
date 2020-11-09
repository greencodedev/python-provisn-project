import discord
import logging
from fileReader import save_discord_obj
from django.utils import timezone
import sys


### In case the bot had to change, modify the TOKEN variable to fit your bot
TOKEN = 'NTI1NzI1NjEyMzQ2ODM0OTY2.Dv60RA.r6YVNgZLUDOP6iluG8el61T0lOY'
DEBUG = False


print("Starting Plutus.Live Discord Bot v1.0")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = discord.Client()

async def get_logs_from(channel):
    async for m in client.logs_from(channel):
        print(m)


@client.event
async def on_message(message):
    ### Ignore own messages
    if message.author == client.user:
        return

    if message.content.startswith('!botreboot'):
        msg = message.author.display_name + " - Forced a bot shutdown!"
        print(msg)
        await client.send_message(message.channel, msg)
        sys.exit(0)

    ### Command for getting main information about the bot
    if message.content.lower().startswith('who are you bot'):
        retMsg = "Plutus.Live Server Bot\n\n"
        retMsg += "Logged in as:\n"
        retMsg += client.user.name + "\n"
        retMsg += client.user.id + "\n"
        retMsg += "---------------------\n"
        retMsg += "In case you changed a previous message or i haven't updated correctly send me\n"
        retMsg += " !forceupdate and i'll try to update again"
        await client.send_message(message.channel, retMsg)
        return

    ### Update preperations
    forceUpdate = False
    if message.content.lower().startswith("!forceupdate"):
        forceUpdate = True

    if forceUpdate:
        print("User " + message.author.display_name + " Forced an Update!")
        await client.send_message(message.channel, "```Update Started!```")

    channels = ['514131268464803860', # Beams
                '514132371075891210', # Events
                '514132408006606848', # News
                '514132452256645121', # Market Intuition
                '514132517721210901', # Member Perks
                '514132608267845633', # Plutus AI
                #'514132793970917406', # Roundtable
                '514132846365900810', # Technical Analysis
                '514132869975900170'  # Token Watchlist
                ]
    logs = []
    for i in range(0, len(channels)):
        logs.append(client.logs_from(discord.Object(id=channels[i]), limit=50))

    ### Here we are actually getting the logs and saving them
    for i in range(0, len(logs)):
        newLogs = []
        log = logs[i]
        async for msg in log:
            curChannel = client.get_channel(msg.channel.id).name
            newLogs.append(
                {'usr': msg.author.display_name,
                 'content': msg.content,
                 'time': msg.timestamp,
                 'channel': curChannel,
                 'attachments': msg.attachments
            })
            save_discord_obj(newLogs, curChannel)

    ### Here we are finishing the whole routine by logging and answering in case of forceUpdate
    if DEBUG:
        print(newLogs)
    if forceUpdate:
        print("Force Update done @ " + str(timezone.now()))
        await client.send_message(message.channel, "```Update Finished @ " + str(timezone.now()) + "```")
    else:
        print("Finished Update @ " + str(timezone.now()))


    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')


### This is actually starting the bot
print("Done loading, waiting for messages...")
client.run(TOKEN)