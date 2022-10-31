import json

from typing import TypedDict
from item import JSONItem, getWowHeadURL
from discord import TextChannel, User, Member
from util import getDataByName, getTrashEmoji, getAcceptEmoji, setDataByName

class LootMessage(TypedDict):
    messageID: int
    guildID: int
    channelID: int
    authorID: int
    item: JSONItem

def getLootMessages() -> list[LootMessage]:
    return getDataByName("lootMessages")

def setLootMessages(lootMessages:list[LootMessage]):
    setDataByName("lootMessages", lootMessages)

def addLootMessage(messageID:int, item:JSONItem, authorID:int, guildID:int, channelID:int):
    lootMessages = getLootMessages()
    lootMessages.append(LootMessage(messageID=messageID, item=item, authorID=authorID, guildID=guildID, channelID=channelID))
    setLootMessages(lootMessages)

def removeLootMessage(messageID:int):
    lootMessages = getLootMessages()
    lootMessage = getLootMessage(messageID)
    if (lootMessage in lootMessages):
        lootMessages.remove(lootMessage)
        setLootMessages(lootMessages)

async def createLootMessage(channel:TextChannel, item:JSONItem, author:User|Member):
    message = await channel.send(getWowHeadURL(item))
    await message.add_reaction(getAcceptEmoji())
    await message.add_reaction(getTrashEmoji())
    addLootMessage(message.id, item, author.id, channel.guild.id, channel.id)
    print(f"created loot message for item {item['name']} in channel {channel.name}")

async def deleteLootMessage(channel:TextChannel, messageID:int):
    message = await channel.fetch_message(messageID)
    if (message.pinned):
        await message.unpin()
    removeLootMessage(message.id)
    await message.delete()
    print(f"deleted loot message in channel {channel.name}")

def getLootMessage(messageID:int) -> LootMessage|None:
    lootMessages = getLootMessages()
    resultLootMessage = None
    for lootMessage in lootMessages:
        if (lootMessage["messageID"] == messageID):
            resultLootMessage = lootMessage
            break
    return resultLootMessage