
import os
import re
import discord
import time

from lootMessage import getLootMessage, createLootMessage, deleteLootMessage, deleteLootMessages
from item import getItemData
from util import getTrashEmoji, getAcceptEmoji
from discord import User, Reaction, Message, MessageType, RawReactionActionEvent
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = Bot(command_prefix="!FISH#", intents=discord.Intents.all())
trashEmoji = getTrashEmoji()
acceptEmoji = getAcceptEmoji()

@bot.command(name="clear", help="clears unpinned loot messages by default - followed by 'all' will clear all loot messages")
async def clear(context:Context, argument:str|None):    
    await deleteLootMessages(context.message.channel, context.guild, argument == "all") # type: ignore
    await context.message.delete()

@bot.command(name="loot", help="copy pasta all the items after this (item names have to be surrounded by [] - all other text will be ignored)")
async def loot(context:Context):
    message = context.message
    pattern = r'\[([\w+\s]+)\]'
    itemNames = re.findall(pattern, message.content)
    for itemName in itemNames:
        item = await getItemData(itemName)
        if (item):
            await createLootMessage(message.channel, item, context.author) # type: ignore
    await message.delete()

@bot.command(name="fetch", help="fetches all given items data")
async def fetch(context:Context):
    message = context.message
    pattern = r'\[([\w+\s]+)\]'
    itemNames = re.findall(pattern, message.content)
    for itemName in itemNames:
        await getItemData(itemName)
    await message.delete()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Connected to Guild {guild.name}')

@bot.event
async def on_message(message:Message):
    # Delete the "Bot pinned message XY" message
    if (message.type == MessageType.pins_add and bot.user != None and message.author.id == bot.user.id):
        await message.delete()
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(event:RawReactionActionEvent):
    guildID = event.guild_id
    channelID = event.channel_id
    messageID = event.message_id

    guild = bot.get_guild(guildID) if guildID else None
    channel = guild.get_channel(channelID) if guild and channelID else None
    message = await channel.fetch_message(messageID) if channel and messageID else None # type: ignore
    lootMessage = getLootMessage(message.id) if message else None

    userID = event.user_id

    if (bot.user != None
        and userID != bot.user.id
        and guild != None
        and message != None
        and lootMessage != None):

        member = await guild.fetch_member(userID)
        emoji = str(event.emoji)
        lootMessage = getLootMessage(message.id)

        if (emoji == acceptEmoji):
            if (not message.pinned):
                await message.pin()
        elif (emoji == trashEmoji and lootMessage != None and userID == lootMessage["authorID"]):
            await deleteLootMessage(message.channel, message.id) # type: ignore
        elif (member):
            await message.remove_reaction(emoji=emoji, member=member)            

@bot.event
async def on_raw_reaction_remove(event:RawReactionActionEvent):
    guildID = event.guild_id
    channelID = event.channel_id
    messageID = event.message_id

    guild = bot.get_guild(guildID) if guildID else None
    channel = guild.get_channel(channelID) if guild and channelID else None
    message = await channel.fetch_message(messageID) if channel and messageID else None # type: ignore

    userID = event.user_id

    if (bot.user != None
        and userID != bot.user.id
        and guild != None
        and message != None):
        
        emoji = str(event.emoji)
        lootMessage = getLootMessage(message.id)

        if (lootMessage != None
            and emoji == acceptEmoji
            and message.pinned):
            for messageReaction in message.reactions:
                if (messageReaction.emoji == acceptEmoji and messageReaction.count == 1):
                    await message.unpin()

bot.run(TOKEN)  # type: ignore